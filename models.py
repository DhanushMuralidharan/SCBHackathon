from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.dialects.oracle import BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import engine
from uuid import uuid4
import datetime

Base = declarative_base()

class Customer(Base):
  __tablename__ = "customer"

  name = Column(Text, nullable=False)
  account_number = Column(Text, nullable=False, unique=True,primary_key=True)
  balance = Column(Float, nullable=False)
  ifsc = Column(Float, nullable=False)
  signature = Column(BLOB, nullable=False)
  date_opened = Column(DateTime, nullable=False)
  processed_ib_cheques = relationship("ProcessedIbCheque", back_populates="customer")

  def __init__(self, name, account_number, balance, ifsc, signature, date_opened):
    self.name = name
    self.account_number = account_number
    self.balance = balance
    self.ifsc = ifsc
    self.signature = signature
    self.date_opened = datetime.datetime.today()


class IbCheque(Base):
  __tablename__ = "ib_cheque"

  cheque_id = Column(Text, nullable=False, unique=True,primary_key=True)
  image = Column(BLOB, nullable=False)
  status = Column(Text, nullable=False)
  ifsc = Column(Float, nullable=False)

  def __init__(self, chqeue_id, image, status):
    self.chqeue_id = str(uuid4())
    self.image = image
    self.status = status

class ObCheque(Base):
  __tablename__ = "ob_cheque"

  cheque_id = Column(Text, nullable=False, unique=True,primary_key=True)
  image = Column(BLOB, nullable=False)
  status = Column(Text, nullable=False)
  ifsc = Column(Float, nullable=False)


  def __init__(self, chqeue_id, image, status):
    self.chqeue_id = str(uuid4())
    self.image = image
    self.status = status

class ProcessedIbCheque(Base):
  __tablename__ = "processed_ib_cheque"

  cheque_number = Column(Text, nullable=False, unique=True,primary_key=True)
  date = Column(Text, nullable=False)
  IFSC = Column(Text, nullable=False)
  acc_no = Column(Text, ForeignKey("customer.account_number"),nullable=False)
  value = Column(Float, nullable=False)
  payee = Column(Text, nullable=False)

  # Foreign key relationship with customer table
  customer = relationship("Customer", back_populates="processed_ib_cheques")

class BankUser(Base):
  __tablename__ = "bank_user"

  BANK = Column(Text,nullable=False)  
  IFSC = Column(Text, nullable=False, unique=True,primary_key=True)
  BRANCH = Column(Text,nullable=False)
  DISTRICT = Column(Text,nullable=False)
  STATE = Column(Text,nullable=False)
  CITY = Column(Text,nullable=False)
  password = Column(Text, nullable=False)
