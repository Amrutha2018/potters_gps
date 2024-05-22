from fastapi import APIRouter
from api import get_gps_pings

router = APIRouter()

router.get("/users/{user_id}/sessions/{session_id}/gps-pings", tags=["User Track"])(get_gps_pings)