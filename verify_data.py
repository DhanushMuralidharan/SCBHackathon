import re
import requests

# for extracting IFSC CODES 
def extract_ifsc_codes(data):
    if_ifsc = False
    for i in data :
        if 'IFSC'.lower() in i.get('text').lower():
            ifsc_match = re.search(r'\b[A-Za-z0-9]{11}\b', i.get('text'))
            if_ifsc = True
    if if_ifsc == True:
        ifsc_code = ifsc_match.group(0)
        return ifsc_code
    else:
        return False

def branch_name(ifsc):
    url = f"https://ifsc.razorpay.com/{ifsc}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data["BRANCH"]


# for extracting Amount
def find_rs(data):
    for i in data : 
        if i.get('text') == '₹' or i.get('text') == 'Rs' : 
            x,y = i['bounding_box'][1]['x'], i['bounding_box'][1]['y']
            return x,y
        else:
            return 0,0

def extract_amount(data):
    x,y = find_rs(data)
    if x != 0 and y !=0:
        y1 = y-10
        y2 = y+10
        for i in data:
            if (i['bounding_box'][0]['x'] > x): 
                if ((i['bounding_box'][0]['y'] > y1) and (i['bounding_box'][0]['y'] < y2)):
                    return i.get('text')
                else:
                    return False
            else:
                return False
    else :
        False
    
#for extracting name
def find_pay(data):
    for i in data : 
        if 'pay' in i.get('text').lower(): 
            x,y = i['bounding_box'][3]['x'], i['bounding_box'][3]['y']
            return x,y
        else:
            return 0,0

def extract_name(data):
    x,y = find_pay(data)
    if x!=0 and y!=0:
        y1 = y-10
        y2 = y+10
        a = []
        for i in data:
            if (i['bounding_box'][3]['x'] > x):
                if ((i['bounding_box'][3]['y'] > y1) and (i['bounding_box'][3]['y'] < y2)):
                    a.append(i)
        if len(a) > 1 : 
            x_coords = [item['bounding_box'][0]['x'] for item in a]
            min_index = x_coords.index(min(x_coords))
            return a[min_index]['text']
        elif len(a) == 1:
            return a[0]['text']
        else: 
            return False
    else : 
        return False

#for extracting amount in words
def find_amountinwords(data):
    for i in data :
        if 'Rupees'.lower() in i.get('text').lower():
            x,y = i['bounding_box'][3]['x'], i['bounding_box'][3]['y']
            return x,y
    return 0,0

def extract_amountinwords(data):
    x,y = find_amountinwords(data)
    if x!=0 and y!=0:
        y1 = y-15
        y2 = y+15
        a = []
        for i in data:
            if (i['bounding_box'][3]['x'] > x):
                if ((i['bounding_box'][3]['y'] > y1) and (i['bounding_box'][3]['y'] < y2)):
                    a.append(i)
        if len(a) > 1 : 
            x_coords = [item['bounding_box'][0]['x'] for item in a]
            min_index = x_coords.index(min(x_coords))
            print(a[min_index]['text'])
        elif len(a) == 1 : 
            return a[0]['text']
        else:
            return False
    return False

#for extracting date
def is_valid_date(date_str):
    try:
        # Extract day, month, and year from the string
        day = int(date_str[:2])
        month = int(date_str[2:4])
        year = int(date_str[4:])
        
        # Check if the year is valid (not earlier than 1900, for example)
        if year < 2010:
            return False
        
        # Import calendar module for additional date checks
        import calendar
        
        # Check if the month and day are within valid ranges
        if month < 1 or month > 12:
            return False
        if day < 1 or day > calendar.monthrange(year, month)[1]:
            return False
        
        return True
    except ValueError:
        # If conversion to integers fails, return False
        return False

def extract_date(data):
    dates = []
    for i in data: 
        if len(i.get('text')) == 8:
            if is_valid_date(i.get('text')):
                dates.append(i.get('text'))
            else:
                return False
    return False

#for extracting cheque number
def find_cheque_number(data):
    # Regular expression pattern to match ⑈ followed by 6 digits
    pattern = r'⑈(\d{6})'
    
    # Search for the pattern in the data
    match = re.search(pattern, data)
    
    if match:
        # Extract the cheque number
        cheque_number = match.group(1)
        return cheque_number
    else:
        return None
    
def extract_cheque_number(data):  
    for i in data : 
        if '⑈' in i.get('text'):
            cheque_number = find_cheque_number(i.get('text'))
            return cheque_number
    else:
        return False
    
#for extracting account number
def find_accountno(data):
    for i in data : 
        if 'A/c'.lower() in i.get('text').lower():
            x,y = i['bounding_box'][2]['x'], i['bounding_box'][2]['y']
            return x,y
        else:
            return 0,0

def extract_accountno(data):
    x,y = find_accountno(data)
    if x !=0 and y!=0:
        y1 = y-20
        y2 = y+20
        a = []
        for i in data:
            if (i['bounding_box'][0]['x'] > x):
                f1 = i['bounding_box'][0]['y']
                f2 = i['bounding_box'][3]['y']
                f = (f1+f2)/2
                if ((f > y1) and (f < y2)):
                    a.append(i)
        if len(a) > 1 : 
            x_coords = [item['bounding_box'][0]['x'] for item in a]
            min_index = x_coords.index(min(x_coords))
            return a[min_index]['text']
        elif len(a) ==1 :
            return a[0]['text']
        else :
            return False
        
    
from num2words import num2words

def compare_amount(amount_in_words, amount_in_number):
    amount_in_words_converted = num2words(amount_in_number,lang='en_IN')
    amount_in_words_normalized = amount_in_words.lower().replace(' ', '')
    amount_in_words_normalized = amount_in_words_normalized.replace('-','').replace(',','')
    amount_in_words_normalized = amount_in_words_normalized .replace('and','').replace('only','')
    amount_in_words_converted_normalized = amount_in_words_converted.lower().replace(' ', '')
    amount_in_words_converted_normalized = amount_in_words_converted_normalized.replace('-','').replace(',','')
    amount_in_words_converted_normalized = amount_in_words_converted_normalized.replace('and','').replace('only','')
    
    # Compare the two strings
    if amount_in_words_normalized == amount_in_words_converted_normalized:
        return True
    else:
        return False

def remove_plural_forms(text):
    # Define the plural forms and their corresponding singular forms
    plural_forms = {"lakhs": "lakh", "crores": "crore"}

    # Replace plural forms with singular forms
    for plural, singular in plural_forms.items():
        text = text.replace(plural, singular)
    return text

def sanitize_number(input_string):
    # Remove non-numeric characters from the input string
    sanitized_string = re.sub(r'[^\d]', '', input_string)
    # Convert the sanitized string to an integer
    sanitized_number = int(sanitized_string)
    return sanitized_number

def check_amount(amount,amountinwords):
    amount_in_words = amountinwords
    amount_in_words_processed = remove_plural_forms(amount_in_words)
    amount_in_number = amount
    sanitized_number = sanitize_number(amount_in_number)

    if compare_amount(amount_in_words_processed, sanitized_number):
        return True
    else:
       return False



from datetime import datetime, timedelta

def is_valid_date(date_string):
    # Define the date formats to parse
    date_formats = ['%d%m%Y', '%d/%m/%Y', '%d-%m-%Y']

    # Get the current date
    current_date = datetime.now()

    # Try parsing the date string using each format
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            break
        except ValueError:
            pass
    else:
        raise ValueError("Invalid date format")

    # Check if the date is not in the future
    if date_obj > current_date:
        return False

    # Calculate the difference in months
    difference = current_date - date_obj
    difference_in_months = (difference.days // 30)  # Approximation of months

    # Check if the difference is less than 3 months
    if difference_in_months < 3:
        return True
    else:
        return False

def check_date(d):

    date_string = d  
    if is_valid_date(date_string):
        return True
    else:
        return False