from config import app,Session
from models import *
from flask import render_template,request,redirect,url_for,session
from extract_data import sample_analyze_all_image_file
from verify_data import *
from io import BytesIO
import os

dbSession = None

@app.before_request
def before_request():
    global dbSession
    dbSession = Session()

@app.teardown_request
def teardown_session(exception=None):
    global dbSession
    dbSession.close()

def out_image_data_extraction(img):
    data =  sample_analyze_all_image_file(img)
    print(data)
    print(type(data))
    ifsc = extract_ifsc_codes(data)
    branch = branch_name(ifsc)
    amount = extract_amount(data)
    amt_inwords = extract_amountinwords(data)
    print(ifsc,branch,amount,amt_inwords)
    # date = extract_date(data)
    if True:
    # check_amount(amount,amt_inwords) : #& check_date(date):
        status = "Processed"
    else:
        status = "Bounced"

    ret_values = {"ifsc":ifsc,"branch":branch,"status":status}
    return ret_values


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
            img = request.files['file']
            filename = img.filename
            img.save(os.path.join('/Users/anantharaman/Documents/StandardChaterHackathon/flask/SCBHackathon/images',filename))
            with open ("/Users/anantharaman/Documents/StandardChaterHackathon/flask/SCBHackathon/images/"+filename,"rb") as f:
                data = out_image_data_extraction(f.read())
            obj = ObCheque(img,ifsc=data["ifsc"],branch=data["branch"],status=data["status"])
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
            image_data = cheques
            
            images = {"image":[i for i in image_data]}
            for i in range(len(image_data)):
                img_stream = BytesIO(image_data[i].image)
                images["image"].append(img_stream)

            return render_template('outgoing_cheques.html',cheques=cheques,images=images)
        
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
