from fastapi import APIRouter
from .api import process_message

router = APIRouter()

# This endpoint is for triggering the worker manually (for testing purposes)
router.post("/process-message/", tags=["Worker"])(process_message)
