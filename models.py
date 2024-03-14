from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.dialects.oracle import BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import engine
from uuid import uuid4
import datetime

Base = declarative_base()

class cheque_deposit(Base):
    