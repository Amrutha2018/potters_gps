from fastapi import APIRouter
from api import receive_gps_ping
from shared_lib.schemas import GpsPingCreate

router = APIRouter()

router.post(
    "/gps-ping/", 
    tags=["GPS Ping"], 
    response_model=GpsPingCreate, 
    summary="Receive a GPS Ping", 
    description="Accepts a GPS ping and publishes it to RabbitMQ."
)(receive_gps_ping)