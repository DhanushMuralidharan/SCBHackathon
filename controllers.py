from config import app,Session
from models import *
from flask import render_template,request,redirect,url_for,session

dbSession = None

@app.before_request
def before_request():
    global dbSession
    dbSession = Session()

@app.teardown_request
def teardown_session(exception=None):
    global dbSession
    dbSession.close()


@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('ifsc')
        password = request.form.get('password')
        user = dbSession.query(BankUser).filter(BankUser.IFSC == username).first()
        if user is not None:
            if user.password == password:
                print("Authenticated successfully!")
                session['user'] = user.IFSC
                return redirect(url_for('dashboard'))
        else:
            print("User not found!")
            return redirect(url_for('login'))
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html')

@app.route('/incoming')
def incoming():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        return render_template('incoming_cheque.html')

@app.route('/outgoing')
def outgoing():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        return render_template('outgoing_cheque.html')

@app.route('/logout')
def logout():
    if 'user' not in session.keys() or session['user'] is None:
        print("No user is currently authenticated to logout!")
        return redirect(url_for('user_login'))
    else:
        session['user'] = None
        print("Logged out successfully!")
        return redirect(url_for('login'))
