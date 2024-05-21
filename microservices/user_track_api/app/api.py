from fastapi import HTTPException, APIRouter
from shared_lib.models import GpsPing, RunSession
from shared_lib.database import SessionLocal
from shared_lib.schemas import GpsPing
from logging_config import logger
from typing import List


router = APIRouter()

@router.get("/gps_pings/{session_id}", response_model=List[GpsPing], summary="Retrieve GPS Pings for a Session", description="Fetches all GPS pings for a given session ID.")
async def get_gps_pings(session_id: int):
    """
    Retrieve GPS pings for a specific session.

    - **session_id**: The ID of the session for which to retrieve GPS pings.
    - **response**: A list of GPS pings including latitude, longitude, and timestamp.
    """
    logger.info(f"Retrieving GPS pings for session ID: {session_id}")
    db = SessionLocal()
    try:
        session = db.query(RunSession).filter(RunSession.id == session_id).first()
        if not session:
            logger.error(f"Session ID {session_id} not found")
            raise HTTPException(status_code=404, detail="Session not found")

        gps_pings = db.query(GpsPing).filter(GpsPing.session_id == session_id).all()
        logger.info(f"Found {len(gps_pings)} GPS pings for session ID {session_id}")

        return gps_pings

    except Exception as e:
        logger.error(f"Error retrieving GPS pings for session ID {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
