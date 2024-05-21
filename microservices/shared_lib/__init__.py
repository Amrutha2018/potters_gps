from .database import SessionLocal, engine, Base
from .models import GpsPing

Base.metadata.create_all(bind=engine)
