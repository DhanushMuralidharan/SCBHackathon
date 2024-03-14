from flask import Flask
from flask import Flask
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

app = Flask(__name__)

current_dir = os.path.abspath(os.path.dirname(__file__))

conn = 'sqlite:///'+ os.path.join(current_dir, 'db.sqlite3')

engine = create_engine(conn)
Session = sessionmaker(bind=engine)
