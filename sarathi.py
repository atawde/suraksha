import qrcode
from PIL import Image
from flask import Flask, render_template, request, redirect, send_file, url_for, session
from jinja2 import Environment, FileSystemLoader
import logging
import sqlite3
import datetime
import secrets

# Data to encode
data = {
        "name":"",
        "address":"",
        "mobile": "",
        "land_line": "",
        "emergency_contact_1":"",
        "emergency_contact_2":"",
        "emergency_contact_3":"",
        "emergency_contact_4":"",
        "blood_group":"",  
        "med_history": "",
        "insurance_provider": "",
        "policy_number": "",
        "vh1_type":"",
        "vh1_make":"",
        "vh1_color":"",
        "vh1_plate":"",
        "vh1_usage":"",
        "vh2_type":"",
        "vh2_make":"",
        "vh2_color":"",
        "vh2_plate":"",
        "vh2_usage":"",
        "date_created":"",
        "date_updated":"",
    }

env = Environment(loader = FileSystemLoader('templates'))
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True  # Show errors
app.secret_key = secrets.token_hex(32)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/how")
def how():
    return render_template("how.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/member")
def member():
    return render_template("member_login.html")

@app.route("/partner")
def partner():
    return render_template("partner_login.html")

@app.route("/register_user", methods=['POST'])
def register_user():
    if request.method == 'POST':
        customer = {"name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1 555 123 4567",
                    "vehicles": [{"make": "Toyota", "model": "Corolla", "reg": "ABC-1234", "year": 2019},
                                 {"make": "Honda", "model": "Civic", "reg": "XYZ-9876", "year": 2020}
                                ],
                    "notes": "Premium customer. Prefers email communication."
                    }
        return render_template('user_details.html', customer=customer)

@app.route("/plogin", methods=['POST'])
def plogin():
    if request.method == 'POST':
        return '<p>Partner logged in </p>'
    
@app.route("/mlogin", methods=['POST'])
def mlogin():
    if request.method == 'POST':
        return '<p>Member logged in </p>'
    
#@app.route("/", methods=['GET', 'POST'])
#def home():
#    return render_template('qr_details.html', img_file="placeholder.png")

@app.route("/submit-form", methods=['POST'])
def generate_qr():
        if request.method == 'POST':
            data["name"] = request.form.get('name')
            data["address"] = request.form.get('address')
            data["mobile"] = request.form.get('mobile')
            data["land_line"] = request.form.get('landl')
            data["emergency_contact_1"] = request.form.get('emer1')
            data["emergency_contact_2"] = request.form.get('emer2')
            data["emergency_contact_3"] = request.form.get('emer3')
            data["emergency_contact_4"] = request.form.get('emer4')
            data["blood_group"] = request.form.get('bgrp')
            data["med_history"] = request.form.get('medh')
            data["insurance_provider"] = request.form.get('insp')
            data["policy_number"] = request.form.get('polnum')
            data["vh1_type"] = request.form.get('vhcletype1')
            data["vh1_make"] = request.form.get('MKMDL1')
            data["vh1_color"] = request.form.get('color1')
            data["vh1_plate"] = request.form.get('plate1')
            data["vh1_usage"] = request.form.get('purpose1')
            data["vh2_type"] = request.form.get('vhcletype2')
            data["vh2_make"] = request.form.get('MKMDL2')
            data["vh2_color"] = request.form.get('color2')
            data["vh2_plate"] = request.form.get('plate2')
            data["vh2_usage"] = request.form.get('purpose2')

            generate_qrcode()
            save_customer_details()
            return render_template('qr_download.html', img_file="my_qrcode.png")
        
#        return render_template('qr_details.html', img_file="placeholder.png")  #for Get method display the same form

@app.route("/download-qr", methods=['POST'])
def download_qr():
     print('QR Image saved !!!')
     return "<p>Your QR code image has been downloaded !!!</p>"

@app.errorhandler(500)
def handle_internal_error(e):
    app.logger.exception("Internal Server Error: %s", e)
    return f"Internal Server Error: {e}", 500

def generate_qrcode():
# Create QR code object
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # size of each box in pixels
        border=4,  # border in boxes
    )

# Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

# Create an image from the QR Code instance
    my_qrcode = qr.make_image(fill_color="black", back_color="white")
# Save the image
    my_qrcode.save("./static/my_qrcode.png")

def save_customer_details():

    create_table_statement = """                      
        CREATE TABLE IF NOT EXISTS qr_code_details (    
            customer_id INTEGER PRIMARY KEY,            
            name text NOT NULL,                
            address text,
            mobile text,
            land_line text,
            emergency_contact_1 text,
            emergency_contact_2 text,
            emergency_contact_3 text,
            emergency_contact_4 text,
            blood_group text,  
            med_history text,
            insurance_provider text,
            policy_number text,
            vh1_type text,
            vh1_make text,
            vh1_color text,
            vh1_plate text,
            vh1_usage text,
            vh2_type text,
            vh2_make text,
            vh2_color text,
            vh2_plate text,
            vh2_usage text,
            date_created DATE, 
            date_updated DATE
        );"""

    today = datetime.date.today().isoformat()
    data['date_created'] = today
    data['date_updated'] = today
    
    cols = ", ".join(data.keys())              
    placeholders = ", ".join([":" + k for k in data.keys()]) 

    insert_statement = f"INSERT INTO qr_code_details ({cols}) VALUES ({placeholders})"
    print(insert_statement)

    try:
        with sqlite3.connect('suraksha_sarthi_db') as conn:
        # create a cursor
            cursor = conn.cursor()
        # execute statements
            cursor.execute(create_table_statement)
            cursor.execute(insert_statement, data)
        # commit the changes
            conn.commit()

        print("QR Details inserted successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to create tables:", e)
     
if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000)
    
