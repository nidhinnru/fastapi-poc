from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from sqlalchemy import and_, or_, desc
from bisect import bisect_left
from pydantic import BaseModel, EmailStr
from .database import Base
from . import models, schemas


def get_audit_api_response_history(db: Session):
    history = db.query(models.audit_api_response_history).order_by(models.audit_api_response_history.timestamp.desc()).limit("10").all()
    return history

def create_audit_base(db: Session, item: schemas.AuditBase, timestamp, source_ip, api_name, payload):
    db_item = models.audit_api_response_history(timestamp=timestamp, source_ip=source_ip, api_name=api_name, payload=payload)
    print(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_audit_api_response_history2(db: Session, item: schemas.AuditBase, timestamp, source_ip, api_name, payload):
    history = db.query(models.audit_api_response_history).order_by(models.audit_api_response_history.timestamp.desc()).limit("10").all()
    db.close()
    db_item = models.audit_api_response_history(timestamp=timestamp, source_ip=source_ip, api_name=api_name, payload=payload)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return history
