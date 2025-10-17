import qrcode
from PIL import Image
from flask import Flask, render_template, request, redirect, send_file, url_for, session, jsonify
from jinja2 import Environment, FileSystemLoader
import logging
import sqlite3
from datetime import timedelta
import datetime
import secrets
import random
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Data to encode
data = {
        "cust_name":"",
        "cust_mobile":"",
        "house": "",
        "building": "",
        "address1":"",
        "address2":"",
        "city":"",
        "state":"",
        "pin":"",  
        "e1_name": "",
        "e1_relation": "",
        "e1_number": "",
        "e2_name": "",
        "e2_relation": "",
        "e2_number": "",
        "e3_name": "",
        "e3_relation": "",
        "e3_number": "",
        "plate":"",
        "vhp":"",
        "vhipn":"",
        "from_dt":"",
        "to_dt":"",
        "bgrp":"",
        "fam_doctor":"",
        "doctor_number":"",
        "med_history":"",
        "hip":"",
        "hipn":"",
        "h_from_dt":"",
        "h_to_dt":"",
        "driver_name":"",
        "driver_mobile":"",
        "d_e1_name":"",
        "d_e1_relation":"",
        "d_e1_number":"",
        "d_e2_name":"",
        "d_e2_relation":"",
        "d_e2_number":"",
        "d_e3_name":"",
        "d_e3_relation":"",
        "d_e3_number":"",
        "d_bgrp":"",
        "d_fam_doctor":"",
        "d_doctor_number":"",
        "d_med_history":"",
        "d_hip":"",
        "d_hipn":"",
        "d_h_from_dt":"",
        "d_h_to_dt":"",
        "date_created":"",
        "date_updated":"",
    }

load_dotenv()
DB_FILE = 'suraksha_sarthi_db'
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
#        customer = {"name": "John Doe",
#                    "email": "john@example.com",
#                    "phone": "+1 555 123 4567",
#                    "vehicles": [{"make": "Toyota", "model": "Corolla", "reg": "ABC-1234", "year": 2019},
#                                 {"make": "Honda", "model": "Civic", "reg": "XYZ-9876", "year": 2020}
#                                ],
#                    "notes": "Premium customer. Prefers email communication."
#                    }
        return render_template("customer_tabs.html", ) # customer=customer)
    
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
def register_customer():
    if request.method == 'POST':
        data["cust_name"] = request.form.get('cust_name')
        data["cust_mobile"] = request.form.get('cust_mobile')
        data["house"] = request.form.get('house')
        data["building"] = request.form.get('building')
        data["address1"] = request.form.get('address1')
        data["address2"] = request.form.get('address2')
        data["city"] = request.form.get('city')
        data["state"] = request.form.get('state')
        data["pin"] = request.form.get('pin')
        data["e1_name"] = request.form.get('e1_name')
        data["e1_relation"] = request.form.get('e1_relation')
        data["e1_number"] = request.form.get('e1_number')
        data["e2_name"] = request.form.get('e2_name')
        data["e2_relation"] = request.form.get('e2_relation')
        data["e2_number"] = request.form.get('e2_number')
        data["e3_name"] = request.form.get('e3_name')
        data["e3_relation"] = request.form.get('e3_relation')
        data["e3_number"] = request.form.get('e3_number')
        data["plate"] = request.form.get('plate')
        data["vhp"] = request.form.get('vhp')
        data["vhipn"] = request.form.get('vhipn')
        data["from_dt"] = request.form.get('from_dt')
        data["to_dt"] = request.form.get('to_dt')
        data["bgrp"] = request.form.get('bgrp')
        data["fam_doctor"] = request.form.get('fam_doctor')
        data["doctor_number"] = request.form.get('doctor_number')
        data["med_history"] = request.form.get('med_history')
        data["hip"] = request.form.get('hip')
        data["hipn"] = request.form.get('hipn')
        data["h_from_dt"] = request.form.get('h_from_dt')
        data["h_to_dt"] = request.form.get('h_to_dt')
        data["driver_name"] = request.form.get('driver_name')
        data["driver_mobile"] = request.form.get('driver_mobile')
        data["d_e1_name"] = request.form.get('d_e1_name')
        data["d_e1_relation"] = request.form.get('d_e1_relation')
        data["d_e1_number"] = request.form.get('d_e1_number')
        data["d_e2_name"] = request.form.get('d_e2_name')
        data["d_e2_relation"] = request.form.get('d_e2_relation')
        data["d_e2_number"] = request.form.get('d_e2_number')
        data["d_e3_name"] = request.form.get('d_e3_name')
        data["d_e3_relation"] = request.form.get('d_e3_relation')
        data["d_e3_number"] = request.form.get('d_e3_number')
        data["d_bgrp"] = request.form.get('d_bgrp')
        data["d_fam_doctor"] = request.form.get('d_fam_doctor')
        data["d_doctor_number"] = request.form.get('d_doctor_number')
        data["d_med_history"] = request.form.get('d_med_history')
        data["d_hip"] = request.form.get('d_hip')
        data["d_hipn"] = request.form.get('d_hipn')
        data["d_h_from_dt"] = request.form.get('d_h_from_dt')
        data["d_h_to_dt"] = request.form.get('d_h_to_dt')

#            generate_qrcode()
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
        CREATE TABLE IF NOT EXISTS customer_details (    
            customer_id INTEGER PRIMARY KEY,            
            cust_name text,
            cust_mobile text,
            house text,
            building text,
            address1 text,
            address2 text,
            city text,
            state text,
            pin text,  
            e1_name text,
            e1_relation text,
            e1_number text,
            e2_name text,
            e2_relation text,
            e2_number text,
            e3_name text,
            e3_relation text,
            e3_number text,
            plate text,
            vhp text,
            vhipn text,
            from_dt text,
            to_dt text,
            bgrp text,
            fam_doctor text,
            doctor_number text,
            med_history text,
            hip text,
            hipn text,
            h_from_dt date,
            h_to_dt date,
            driver_name text,
            driver_mobile text,
            d_e1_name text,
            d_e1_relation text,
            d_e1_number text,
            d_e2_name text,
            d_e2_relation text,
            d_e2_number text,
            d_e3_name text,
            d_e3_relation text,
            d_e3_number text,
            d_bgrp text,
            d_fam_doctor text,
            d_doctor_number text,
            d_med_history text,
            d_hip text,
            d_hipn text,
            d_h_from_dt date,
            d_h_to_dt date,
            date_created date,
            date_updated date,
        );"""

    today = datetime.date.today().isoformat()
    data['date_created'] = today
    data['date_updated'] = today
    
    cols = ", ".join(data.keys())              
    placeholders = ", ".join([":" + k for k in data.keys()]) 

    insert_statement = f"INSERT INTO customer_details ({cols}) VALUES ({placeholders})"
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

        print("Customer Details inserted successfully.")
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
    
