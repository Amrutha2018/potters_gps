from fastapi import APIRouter
from api import process_message
from shared_lib.schemas import GpsPing

router = APIRouter()

# This endpoint is for triggering the worker manually (for testing purposes)
router.post(
    "/process-message/", 
    tags=["Worker"],
    response_model=GpsPing,
    summary="Process GPS Ping From RabbitMq",
    description="Process and save GPS Pings recieved from RabbitMq"
)(process_message)
