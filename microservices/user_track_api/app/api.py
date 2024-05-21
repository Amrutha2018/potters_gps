from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from shared_lib import GpsPing, RunSession
from shared_lib import get_db
from main import logger

async def get_gps_pings(session_id: int, db: Session = Depends(get_db)):
    logger.info(f"Retrieving GPS pings for session ID: {session_id}")
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
