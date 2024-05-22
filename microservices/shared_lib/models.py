from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    sessions = relationship("RunSession", back_populates="user")

class RunSession(Base):
    __tablename__ = "run_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    gps_pings = relationship("GpsPing", back_populates="session")
    user = relationship("User", back_populates="sessions")

class GpsPing(Base):
    __tablename__ = "gps_pings"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('run_sessions.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    session = relationship("RunSession", back_populates="gps_pings")