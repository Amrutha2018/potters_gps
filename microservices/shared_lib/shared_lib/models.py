from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class RunSession(Base):
    __tablename__ = 'run_sessions'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    gps_pings = relationship("GpsPing", back_populates="session")

class GpsPing(Base):
    __tablename__ = 'gps_pings'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('run_sessions.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    session = relationship("RunSession", back_populates="gps_pings")