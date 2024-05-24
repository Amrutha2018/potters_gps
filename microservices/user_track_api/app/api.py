from fastapi import HTTPException, APIRouter
from sqlalchemy.orm import Session
from shared_lib.models import GpsPing, RunSession, User
from shared_lib.database import SessionLocal
from shared_lib.schemas import GpsPing as GpsPingSchema
from logging_config import logger
from typing import List


router = APIRouter()

@router.get("/users/{user_id}/sessions/{session_id}/gps-pings", response_model=List[GpsPingSchema], summary="Retrieve GPS Pings for a User Session", description="Fetches all GPS pings for a given user and session ID.")
async def get_gps_pings(user_id: int, session_id: int):
    """
    Retrieve GPS pings for a specific user and session.

    - **user_id**: The ID of the user for whom to retrieve GPS pings.
    - **session_id**: The ID of the session for which to retrieve GPS pings.
    - **response**: A list of GPS pings including latitude, longitude, and timestamp.
    """
    logger.info(f"Retrieving GPS pings for user ID: {user_id}, session ID: {session_id}")
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        session = db.query(RunSession).filter(RunSession.id == session_id, RunSession.user_id == user_id).first()
        if not session:
            logger.error(f"Session ID {session_id} not found for user ID {user_id}")
            raise HTTPException(status_code=404, detail="Session not found")

        gps_pings = db.query(GpsPing).filter(GpsPing.session_id == session_id).all()
        logger.info(f"Found {len(gps_pings)} GPS pings for user ID {user_id}, session ID {session_id}")

        return gps_pings

    except Exception as e:
        logger.error(f"Error retrieving GPS pings for user ID {user_id}, session ID {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()
