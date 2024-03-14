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

@app.route('/incoming/add',methods=['GET','POST'])
def Addincoming():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('add_in_ch.html')
        elif request.method == 'POST':
            obj = IbCheque(request.files['file'].read(),'pending',session['user'])
            dbSession.add(obj)
            dbSession.commit()
            return redirect(url_for('incoming'))

@app.route('/outgoing/add',methods=['POST','GET'])
def Addoutgoing():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('add_out_ch.html')
        elif request.method == 'POST':
            obj = ObCheque(request.files['file'].read(),'pending',session['user'])
            dbSession.add(obj)
            dbSession.commit()
            return redirect(url_for('outgoing'))
        
@app.route('/outgoing',methods=['GET'])
def outgoing():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            cheques = dbSession.query(ObCheque).all()
            return render_template('outgoing_cheques.html',cheques=cheques)
        
@app.route('/incoming',methods=['GET'])
def incoming():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            cheques = dbSession.query(IbCheque).all()
            return render_template('incoming_cheques.html',cheques=cheques)
        

@app.route('/logout')
def logout():
    if 'user' not in session.keys() or session['user'] is None:
        print("No user is currently authenticated to logout!")
        return redirect(url_for('user_login'))
    else:
        session['user'] = None
        print("Logged out successfully!")
        return redirect(url_for('login'))
