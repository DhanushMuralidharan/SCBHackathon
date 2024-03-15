from flask import Flask
from flask import Flask
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

app = Flask(__name__)

app.jinja_env.filters['zip'] = zip

app.config['SECRET_KEY']= os.getenv('SESSIONPW')
app.config['SECURITY_PASSWORD_SALT'] =  os.getenv('SALT')
app.app_context().push()

current_dir = os.path.abspath(os.path.dirname(__file__))

conn = 'sqlite:///'+ os.path.join(current_dir, 'db.sqlite3')

engine = create_engine(conn)
Session = sessionmaker(bind=engine)
