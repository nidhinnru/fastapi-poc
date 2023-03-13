"""
the following code was obtained from the fast aspi tutorial
https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-database-url-for-sqlalchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import os

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL') 
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

