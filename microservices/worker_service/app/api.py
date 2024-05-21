import json
from datetime import datetime
import aio_pika
from sqlalchemy.exc import SQLAlchemyError
from shared_lib.models import RunSession, GpsPing
from logging_config import logger
from shared_lib.database import SessionLocal
from shared_lib.schemas import GpsPingCreate

async def process_message(message: GpsPingCreate):
    logger.info("Received a new message from RabbitMQ")
    async with message.process():
        db = SessionLocal()
        try:
            data = json.loads(message.body)
            logger.debug(f"Processing message: {data}")

            # Parse and validate the message body
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            timestamp = datetime.fromisoformat(data.get("timestamp"))
            start = data.get("start")
            end = data.get("end")

            # Ensure all required fields are present
            if not all([latitude, longitude, timestamp]):
                logger.error("Message is missing required fields")
                return

            # Handle session logic
            session = None
            if start:
                session = RunSession(start_time=timestamp, end_time=None)
                db.add(session)
                db.commit()
                db.refresh(session)
                logger.info(f"Started new session: {session.id}")
            else:
                session = db.query(RunSession).filter(RunSession.end_time == None).first()
                if not session:
                    session = RunSession(start_time=datetime.utcnow(), end_time=None)
                    db.add(session)
                    db.commit()
                    db.refresh(session)
                    logger.info(f"Started new orphan session: {session.id}")

            if end:
                session.end_time = timestamp
                db.commit()
                logger.info(f"Ended session: {session.id}")

            # Create GPS Ping
            db_ping = GpsPing(
                session_id=session.id,
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp
            )
            db.add(db_ping)
            db.commit()
            logger.info(f"Saved GPS ping: {db_ping.id}")

        except SQLAlchemyError as db_err:
            logger.error(f"Database error: {db_err}")
            db.rollback()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
        finally:
            db.close()