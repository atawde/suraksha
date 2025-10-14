import qrcode
from PIL import Image
from flask import Flask, render_template, request, redirect, send_file, url_for, session, jsonify
from jinja2 import Environment, FileSystemLoader
import logging
import sqlite3
from datetime import datetime, timedelta
import secrets
import random
from twilio.rest import Client
from dotenv import load_dotenv
import os

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

load_dotenv()
DB_FILE = 'suraksha_sarthi_db'
#TWILIO_SID = "AC3118fa504f26fb3180826f345db47089"
#TWILIO_TOKEN = "15e174d037ffed7c953753255fec8763"
#TWILIO_PHONE = "+12294715420"
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE")

print(f"SID {account_sid} token {auth_token} phone {twilio_phone}")

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
    return render_template("request_otp.html")

@app.route("/partner")
def partner():
    return render_template("partner_login.html")

@app.route("/manage_otp", methods=['POST'])
def manage_otp():
    if request.method == 'POST':
        return render_template("request_otp.html")

@app.route("/register_user", methods=['GET'])
def register_user():
    if request.method == 'GET':
        customer = {"name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1 555 123 4567",
                    "vehicles": [{"make": "Toyota", "model": "Corolla", "reg": "ABC-1234", "year": 2019},
                                 {"make": "Honda", "model": "Civic", "reg": "XYZ-9876", "year": 2020}
                                ],
                    "notes": "Premium customer. Prefers email communication."
                    }
        return render_template("customer_tabs.html", customer=customer)
    
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
        with sqlite3.connect(DB_FILE) as conn:
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

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            otp TEXT NOT NULL,
            expires_at DATETIME NOT NULL
        )
        """)
        conn.commit()

init_db()

# --- OTP Generator ---
def generate_otp():
    return str(random.randint(100000, 999999))

# --- Request OTP ---
@app.route("/request_otp", methods=["POST"])
def request_otp():
    phone = request.form.get("mnumber")
    if not phone:
        return f"error: phone required"

    with sqlite3.connect(DB_FILE) as conn:
        # 1. Delete expired OTPs before creating a new one
        conn.execute("DELETE FROM otps WHERE expires_at < ?", (datetime.utcnow(),))
        
        # 2. Generate OTP
        otp = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        conn.execute("INSERT INTO otps (phone, otp, expires_at) VALUES (?, ?, ?)",
                     (phone, otp, expires_at))
        conn.commit()

    # In production, send OTP via SMS API (Twilio, MSG91, etc.)
    return render_template("verify_otp.html", mnumber=phone, otp = otp)
    
# --- Verify OTP ---
@app.route("/send_otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    phone = data.get("phone")
    otp = data.get("otp")

    if not phone or not otp:
        return jsonify({"error": "Missing phone or otp"}), 400

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your verification code is {otp}",
        from_=twilio_phone,
        to=phone
    )

    print("Sent OTP:", otp, "to", phone)
    return jsonify({"message": "OTP sent successfully"})


if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
