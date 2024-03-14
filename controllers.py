from config import app

@app.route('/')
def index():
    return "Welcome to SCB Hackathon Home Page"