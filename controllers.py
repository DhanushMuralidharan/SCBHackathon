from config import app,Session
from models import *
from flask import render_template,request,redirect,url_for,session
from extract_data import sample_analyze_all_image_file
from verify_data import *
from io import BytesIO
import os
import base64
from extract_signature import *
from verify_signature import *
import sqlite3
from verify_acc_check import *

dbSession = None

@app.before_request
def before_request():
    global dbSession
    dbSession = Session()

@app.teardown_request
def teardown_session(exception=None):
    global dbSession
    dbSession.close()

def extract_sign_from_db(account_number):
    print("")
    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT signature FROM customer WHERE account_number = ?", (account_number,))
    signature_data = c.fetchone()
    conn.close()
    if signature_data:
        signature_bytes = signature_data[0]
        print(signature_bytes)
        image = open("images/sign_db.jpg","wb")
        image.write(signature_bytes)

        return True
    else:
        print("Signature not found for account number:", account_number)
        return None
    
def out_image_data_extraction(img):
    data =  sample_analyze_all_image_file(img)
    print(data)
    print(type(data))
    ifsc = extract_ifsc_codes(data)
    branch = branch_name(ifsc)
    amount = extract_amount(data)
    amt_inwords = extract_amountinwords(data)
    accountNo = extract_accountno(data)
    print(ifsc,branch,amount,amt_inwords)

    date = extract_date(data)
    if check_amount(amount,amt_inwords) and check_date(date):
        status = "Processed"                                
    else:
        status = "Bounced"

    ret_values = {"ifsc":ifsc,"branch":branch,"status":status,"accountNo":accountNo}
    return ret_values

def inc_image_data_extraction(img,img_path):
    data =  sample_analyze_all_image_file(img)
    print(data)
    print(type(data))
    ifsc = extract_ifsc_codes(data)
    branch = branch_name(ifsc)
    amount = extract_amount(data)
    amt_inwords = extract_amountinwords(data)
    accountNo = extract_accountno(data)
    print(ifsc,branch,amount,amt_inwords)

    date = extract_date(data)
    # if check_amount(amount,amt_inwords): #and check_date(date):
    if True:
        extract_sign(img_path)
        sign_image = extract_sign_from_db(accountNo)
        if sign_image:
            # print("hey")
            if verify_sign(r"images/signature/cropped_image.png",r"images/sign_db.jpg"):
                # print("verified")
                status = "Processed"
                remarks = "Verified"
            else:
                status = "Bounced"
                remarks = "Signature not matched"

        else:
            status = "Bounced" 
            remarks = "Signature not found" 

    else:
        status = "Bounced"
        remarks = "Invalid Data"

    
    # if verify_credit_type(img_path):
    if True:
        credit_type = "Account"
    else:
        credit_type = "Cash/Account"
    ret_values = {"ifsc":ifsc,"credit_type":credit_type,"status":status,"accountNo":accountNo,"remarks":remarks}
    return ret_values



def convert_image_to_base64(image_data):
    # Convert the image bytes to a Base64-encoded string
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image

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
            img = request.files['file']
            filename = img.filename
            img.save(os.path.join('images',filename))
            img_path = "images/"+filename
            with open (img_path,"rb") as f:
                img_data=f.read()
                data = inc_image_data_extraction(img_data,img_path)
                
            obj = IbCheque(image=img_data,ifsc=data["ifsc"],status=data["status"],accountNo=data["accountNo"],credit_type=data["credit_type"],remarks=data["remarks"])
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
            img.save(os.path.join('images',filename))
            with open ("images/"+filename,"rb") as f:
                img_data=f.read()
                data = out_image_data_extraction(img_data)
                
            print("image_data",img_data)
            obj = ObCheque(image=img_data,ifsc=data["ifsc"],branch=data["branch"],status=data["status"],accountNo=data["accountNo"])
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
            # print(type(image_data[0].image))
            images = []
            img_displayed = {"images":[]}
            for i in range(len(image_data)):
                img_stream = convert_image_to_base64(image_data[i].image)
                images.append(img_stream)
            # print(images[0])
            return render_template('outgoing_cheques.html',cheques=cheques,images=images)
        
@app.route('/incoming',methods=['GET'])
def incoming():
    if 'user' not in session.keys() or session['user'] is None:
        print("You must be authenticated first!")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            cheques = dbSession.query(IbCheque).all()
            image_data = cheques
            # print(type(image_data[0].image))
            images = []
            img_displayed = {"images":[]}
            for i in range(len(image_data)):
                img_stream = convert_image_to_base64(image_data[i].image)
                images.append(img_stream)
            return render_template('incoming_cheques.html',cheques=cheques,images=images)
        
        

@app.route('/logout')
def logout():
    if 'user' not in session.keys() or session['user'] is None:
        print("No user is currently authenticated to logout!")
        return redirect(url_for('user_login'))
    else:
        session['user'] = None
        print("Logged out successfully!")
        return redirect(url_for('login'))
