from config import app
from models import *
from flask import render_template

@app.route('/')
def index():
    return "Welcome to SCB Hackathon Home Page"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/incoming')
def incoming():
    return render_template('incoming_cheque.html')

@app.route('/outgoing')
def outgoing():
    return render_template('outgoing_cheque.html')