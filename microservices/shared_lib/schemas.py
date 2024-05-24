from pydantic import BaseModel, model_validator, ValidationError
from datetime import datetime
from typing import Optional

class GpsPingBase(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime

class GpsPingCreate(GpsPingBase):
    start: Optional[bool] = False
    end: Optional[bool] = False
    user_id: Optional[int] = None
    user_email: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def check_user_id_or_email(cls, values):
        user_id, user_email = values.get('user_id'), values.get('user_email')
        if not user_id and not user_email:
            raise ValueError('Either user_id or user_email must be provided')
        return values

class GpsPing(GpsPingBase):
    id: int
    session_id: int

    class Config:
        orm_mode = True
