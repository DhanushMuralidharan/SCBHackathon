from config import app
from models import *

@app.route('/')
def index():
    return "Welcome to SCB Hackathon Home Page"