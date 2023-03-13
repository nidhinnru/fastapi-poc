from pydantic import BaseModel
from typing import List
from .database import Base


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import ForeignKeyConstraint
import enum

class audit_api_response_history(Base):

    __tablename__ = "audit_api_response_history"
    timestamp = Column(String, primary_key=True, unique=True, index=True)
    source_ip = Column(String, unique=False)
    api_name = Column(String, unique=False)
    payload = Column(String, unique=False)
