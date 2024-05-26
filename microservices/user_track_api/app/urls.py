from fastapi import APIRouter
from api import get_gps_pings
from typing import List
from shared_lib.schemas import GpsPing as GpsPingSchema

router = APIRouter()

router.get(
    "/users/{user_id}/sessions/{session_id}/gps-pings", 
    tags=["User Track"], 
    response_model=List[GpsPingSchema], 
    summary="Retrieve GPS Pings for a User Session", 
    description="Fetches all GPS pings for a given user and session ID."
)(get_gps_pings)