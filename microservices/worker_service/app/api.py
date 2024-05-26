import json
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from shared_lib.models import RunSession, GpsPing, User
from logging_config import logger
from shared_lib.database import SessionLocal
from shared_lib.schemas import GpsPingCreate
from pydantic import ValidationError

async def process_message(message: GpsPingCreate):
    logger.info("Received a new message from RabbitMQ")
    async with message.process():
        db = SessionLocal()
        try:
            data = json.loads(message.body.decode())
            logger.debug(f"Processing message: {data}")

            try:
                ping = GpsPingCreate(**data)
            except ValidationError as e:
                logger.error("Vaidation error: {e.json()}")
                return

            # Start a new transaction
            with db.begin():
                # Handle user logic
                user = None
                if ping.user_id:
                    user = db.query(User).filter(User.id == ping.user_id).first()
                if ping.user_email:
                    user = db.query(User).filter(User.email == ping.user_email).first()
                    if not user:
                        # Create a new user if not exists
                        user = User(email=ping.user_email, name=f"User {ping.user_email}")
                        db.add(user)
                        db.flush()  # Use flush to assign ID without committing
                        logger.info(f"Created new user: {user.id}")

                if not user:
                    logger.error("User not found and no user email provided")
                    return

                # Handle session logic
                session = None
                open_sessions = db.query(RunSession).filter(RunSession.user_id == user.id, RunSession.end_time == None).all()

                if ping.start:
                    if open_sessions:
                        # End all open sessions before starting a new one
                        for open_session in open_sessions:
                            open_session.end_time = ping.timestamp
                            logger.info(f"Ended session: {open_session.id}")
                        db.flush()  # Use flush to update without committing

                    # Start a new session
                    session = RunSession(user_id=user.id, start_time=ping.timestamp, end_time=None)
                    db.add(session)
                    db.flush()  # Use flush to assign ID without committing
                    logger.info(f"Started new session: {session.id}")
                elif ping.end:
                    if open_sessions:
                        # End all open sessions and attach the current ping to the latest session
                        for open_session in open_sessions:
                            open_session.end_time = ping.timestamp
                            logger.info(f"Ended session: {open_session.id}")
                        db.flush()  # Use flush to update without committing
                        session = open_sessions[-1]  # Use the latest session for the ping
                    else:
                        # No open sessions, create a session with start and end as current timestamp
                        session = RunSession(user_id=user.id, start_time=ping.timestamp, end_time=ping.timestamp)
                        db.add(session)
                        db.flush()  # Use flush to assign ID without committing
                        logger.info(f"Created new session with start and end time: {session.id}")
                else:
                    if open_sessions:
                        # Use the latest open session and end all others
                        session = open_sessions[-1]
                        for open_session in open_sessions[:-1]:
                            open_session.end_time = ping.timestamp
                            logger.info(f"Ended session: {open_session.id}")
                        db.flush()  # Use flush to update without committing
                        logger.info(f"Using latest open session: {session.id}")
                    else:
                        # No start and no end, no open session exists, create an orphan session
                        session = RunSession(user_id=user.id, start_time=datetime.utcnow(), end_time=None)
                        db.add(session)
                        db.flush()  # Use flush to assign ID without committing
                        logger.info(f"Started new orphan session: {session.id}")

                # Create GPS Ping
                db_ping = GpsPing(
                    session_id=session.id,
                    latitude=ping.latitude,
                    longitude=ping.longitude,
                    timestamp=ping.timestamp
                )
                db.add(db_ping)
                db.flush()  # Use flush to assign ID without committing
                logger.info(f"Saved GPS ping: {db_ping.id}")

        except SQLAlchemyError as db_err:
            logger.error(f"Database error: {db_err}")
            db.rollback()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
        finally:
            db.close()