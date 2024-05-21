from fastapi import APIRouter
from .api import receive_gps_ping

router = APIRouter()

router.post("/gps-ping/", tags=["GPS Ping"])(receive_gps_ping)