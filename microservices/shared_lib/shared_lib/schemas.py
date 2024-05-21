from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GpsPingBase(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime

class GpsPingCreate(GpsPingBase):
    start: Optional[bool] = False
    end: Optional[bool] = False

class GpsPing(GpsPingBase):
    id: int
    session_id: int

    class Config:
        orm_mode = True
