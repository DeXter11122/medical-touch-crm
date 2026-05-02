from flask import Flask, render_template_string, request, jsonify, send_from_directory, session, redirect, url_for
import json
import os
from datetime import datetime
import time
from functools import wraps
from collections import Counter

app = Flask(__name__)
app.secret_key = 'medicaltouchsecretkey2024'

DATA_FILE = 'salon_data.json'
NOTIFICATIONS_FILE = 'notifications.json'

ADMIN_USERNAME = "medicaltouch"
ADMIN_PASSWORD = "admin123"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin_login_page'))
        return f(*args, **kwargs)
    return decorated_function

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'customers': [],
        'appointments': [],
        'cancelled_appointments': [],
        'materials': {
            'Nails': {'cost': 500, 'items': ['Gel Polish', 'Acrylic Powder', 'Tips', 'Files', 'Buffer', 'Top Coat', 'Base Coat']},
            'Lashes': {'cost': 300, 'items': ['Lash Glue', 'Lashes', 'Tweezers', 'Primer', 'Sealant', 'Remover']},
            'Skincare': {'cost': 400, 'items': ['Serums', 'Masks', 'MesoNeedles', 'Products', 'Cleanser', 'Moisturizer']},
            'Wax': {'cost': 200, 'items': ['Wax Beans', 'Strips', 'Oil', 'Pre/Post Care', 'Applicators', 'Wax Warmer']}
        },
        'services': [
            # NAILS - 20 services
            {'id': '1', 'name': 'Full Set GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5, 'description': 'Long-lasting gel polish with perfect shine'},
            {'id': '2', 'name': 'Full Set Fiber GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5, 'description': 'Strengthening fiber gel for weak nails'},
            {'id': '3', 'name': 'Full Set Polygel + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5, 'description': 'Lightweight polygel extension'},
            {'id': '4', 'name': 'Full Set Gel-X + Color Gel', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 4, 'description': 'Quick gel extension application'},
            {'id': '5', 'name': 'Full Set Acrylic', 'price': 40, 'duration': 75, 'category': 'Nails', 'material_cost': 6, 'description': 'Classic acrylic nails'},
            {'id': '6', 'name': 'Dipping Powder GEL', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 4, 'description': 'Strong dip powder system'},
            {'id': '7', 'name': 'Full Set Lucid GEL', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 4, 'description': 'Natural look gel nails'},
            {'id': '8', 'name': 'Rubber Base + Color Gel', 'price': 20, 'duration': 45, 'category': 'Nails', 'material_cost': 3, 'description': 'Flexible rubber base for weak nails'},
            {'id': '9', 'name': 'Gel Color + Base Gel', 'price': 15, 'duration': 30, 'category': 'Nails', 'material_cost': 2, 'description': 'Simple gel color change'},
            {'id': '10', 'name': 'Ombre Gelish + Rubber Base', 'price': 15, 'duration': 45, 'category': 'Nails', 'material_cost': 3, 'description': 'Beautiful ombre effect'},
            {'id': '11', 'name': 'French Gelish + Rubber Base', 'price': 18, 'duration': 45, 'category': 'Nails', 'material_cost': 3, 'description': 'Classic french manicure'},
            {'id': '12', 'name': 'Refill GEL', 'price': 22, 'duration': 45, 'category': 'Nails', 'material_cost': 3, 'description': 'Gel nail refill service'},
            {'id': '13', 'name': 'Remove GEL + Manicure', 'price': 15, 'duration': 30, 'category': 'Nails', 'material_cost': 2, 'description': 'Safe gel removal with manicure'},
            {'id': '14', 'name': 'Manicure + Pose', 'price': 10, 'duration': 30, 'category': 'Nails', 'material_cost': 2, 'description': 'Basic manicure with polish'},
            {'id': '15', 'name': 'Pedicure + Pose', 'price': 15, 'duration': 45, 'category': 'Nails', 'material_cost': 3, 'description': 'Relaxing pedicure treatment'},
            {'id': '16', 'name': 'Paraffin', 'price': 8, 'duration': 20, 'category': 'Nails', 'material_cost': 1, 'description': 'Paraffin wax hand treatment'},
            {'id': '17', 'name': 'Pose Verni', 'price': 5, 'duration': 15, 'category': 'Nails', 'material_cost': 1, 'description': 'Regular polish application'},
            {'id': '18', 'name': 'French Verni', 'price': 10, 'duration': 20, 'category': 'Nails', 'material_cost': 1, 'description': 'French polish manicure'},
            {'id': '19', 'name': 'Fake Nails + Color', 'price': 15, 'duration': 45, 'category': 'Nails', 'material_cost': 3, 'description': 'Press-on nail application'},
            {'id': '20', 'name': 'Special Nail Art', 'price': 15, 'duration': 30, 'category': 'Nails', 'material_cost': 3, 'description': 'Custom nail art design'},
            # LASHES - 5 services
            {'id': '21', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes', 'material_cost': 5, 'description': 'Natural classic lash extensions'},
            {'id': '22', 'name': 'Full Set Lashes Volume', 'price': 38, 'duration': 90, 'category': 'Lashes', 'material_cost': 5, 'description': 'Fluffy volume lash fans'},
            {'id': '23', 'name': 'Full Set Lashes Mega Volume', 'price': 45, 'duration': 105, 'category': 'Lashes', 'material_cost': 6, 'description': 'Dramatic mega volume lashes'},
            {'id': '24', 'name': 'Refill Lashes', 'price': 25, 'duration': 45, 'category': 'Lashes', 'material_cost': 3, 'description': 'Lash extension refill'},
            {'id': '25', 'name': 'Removal Lashes', 'price': 20, 'duration': 30, 'category': 'Lashes', 'material_cost': 2, 'description': 'Safe lash removal'},
            # SKINCARE - 16 services
            {'id': '26', 'name': 'Facial Classic', 'price': 35, 'duration': 60, 'category': 'Skincare', 'material_cost': 4, 'description': 'Deep cleansing facial'},
            {'id': '27', 'name': 'Hydra Facial', 'price': 55, 'duration': 75, 'category': 'Skincare', 'material_cost': 8, 'description': 'Hydradermabrasion facial'},
            {'id': '28', 'name': 'Medical Facial + MesoTherapy', 'price': 65, 'duration': 90, 'category': 'Skincare', 'material_cost': 10, 'description': 'Advanced medical facial with mesotherapy'},
            {'id': '29', 'name': 'HIFU', 'price': 100, 'duration': 90, 'category': 'Skincare', 'material_cost': 5, 'description': 'High intensity focused ultrasound lifting'},
            {'id': '30', 'name': 'Mesopen Whitening', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Skin whitening mesotherapy'},
            {'id': '31', 'name': 'Mesopen Acne', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Acne treatment mesotherapy'},
            {'id': '32', 'name': 'Mesopen Lifting Face', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Face lifting mesotherapy'},
            {'id': '33', 'name': 'Mesopen Dark Circle', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Under-eye dark circle treatment'},
            {'id': '34', 'name': 'Mesopen Lip Whitening', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Lip lightening treatment'},
            {'id': '35', 'name': 'Mesopen Hair Loss', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Hair loss treatment'},
            {'id': '36', 'name': 'Mesopen Hair Grow', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Hair growth stimulation'},
            {'id': '37', 'name': 'Mesopen Cellulite', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8, 'description': 'Cellulite reduction treatment'},
            {'id': '38', 'name': 'Meso botox Injection', 'price': 100, 'duration': 60, 'category': 'Skincare', 'material_cost': 15, 'description': 'Mesobotax injection'},
            {'id': '39', 'name': 'Meso lipo double Chin', 'price': 100, 'duration': 60, 'category': 'Skincare', 'material_cost': 15, 'description': 'Double chin fat reduction'},
            {'id': '40', 'name': 'Meso Fats (5 Sessions)', 'price': 200, 'duration': 60, 'category': 'Skincare', 'material_cost': 50, 'description': '5 session fat reduction package'},
            {'id': '41', 'name': 'Meso Melasma Injection', 'price': 100, 'duration': 60, 'category': 'Skincare', 'material_cost': 15, 'description': 'Melasma treatment injection'},
            # WAX - 19 services
            {'id': '42', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax', 'material_cost': 3, 'description': 'Complete body waxing'},
            {'id': '43', 'name': 'Full Face + Neck Wax', 'price': 15, 'duration': 30, 'category': 'Wax', 'material_cost': 1, 'description': 'Face and neck wax'},
            {'id': '44', 'name': 'Full Back Wax', 'price': 18, 'duration': 30, 'category': 'Wax', 'material_cost': 1, 'description': 'Full back waxing'},
            {'id': '45', 'name': 'Lower Back Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1, 'description': 'Lower back wax'},
            {'id': '46', 'name': 'Half Back Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1, 'description': 'Upper or lower back'},
            {'id': '47', 'name': 'Full Belly Wax', 'price': 18, 'duration': 30, 'category': 'Wax', 'material_cost': 1, 'description': 'Full stomach wax'},
            {'id': '48', 'name': 'Chest Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1, 'description': 'Chest hair removal'},
            {'id': '49', 'name': 'Full Arms Wax', 'price': 12, 'duration': 30, 'category': 'Wax', 'material_cost': 1, 'description': 'Both arms full wax'},
            {'id': '50', 'name': 'Half Arms Wax', 'price': 8, 'duration': 20, 'category': 'Wax', 'material_cost': 1, 'description': 'Forearm or upper arm'},
            {'id': '51', 'name': 'Under Arms Wax', 'price': 6, 'duration': 15, 'category': 'Wax', 'material_cost': 1, 'description': 'Underarm waxing'},
            {'id': '52', 'name': 'Full Legs Wax', 'price': 17, 'duration': 45, 'category': 'Wax', 'material_cost': 1, 'description': 'Complete leg wax'},
            {'id': '53', 'name': 'Half Legs Wax', 'price': 11, 'duration': 30, 'category': 'Wax', 'material_cost': 1, 'description': 'Lower or upper leg'},
            {'id': '54', 'name': 'Full Bikini Wax', 'price': 23, 'duration': 30, 'category': 'Wax', 'material_cost': 2, 'description': 'Full bikini wax'},
            {'id': '55', 'name': 'Bikini Line Wax', 'price': 16, 'duration': 20, 'category': 'Wax', 'material_cost': 1, 'description': 'Basic bikini line'},
            {'id': '56', 'name': 'Eyebrow Classic Wax', 'price': 4, 'duration': 10, 'category': 'Wax', 'material_cost': 0.5, 'description': 'Eyebrow wax shaping'},
            {'id': '57', 'name': 'Eyebrow Waxing', 'price': 6, 'duration': 10, 'category': 'Wax', 'material_cost': 0.5, 'description': 'Eyebrow cleanup'},
            {'id': '58', 'name': 'Lips Classic Wax', 'price': 3, 'duration': 5, 'category': 'Wax', 'material_cost': 0.5, 'description': 'Upper lip wax'},
            {'id': '59', 'name': 'Lips Wax', 'price': 5, 'duration': 10, 'category': 'Wax', 'material_cost': 0.5, 'description': 'Upper and lower lip'},
            {'id': '60', 'name': 'Nose + Chin Wax', 'price': 7, 'duration': 15, 'category': 'Wax', 'material_cost': 0.5, 'description': 'Nose and chin wax'},
        ]
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_notifications():
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notifications(notifications):
    with open(NOTIFICATIONS_FILE, 'w') as f:
        json.dump(notifications, f, indent=2)

def add_notification(message):
    notifs = load_notifications()
    notifs.insert(0, {
        'id': str(int(time.time())),
        'message': message,
        'time': datetime.now().strftime('%I:%M %p'),
        'read': False
    })
    save_notifications(notifs[:50])

def check_double_booking(staff_id, datetime_str):
    data = load_data()
    for a in data['appointments']:
        if a.get('staff_id') == staff_id and a.get('datetime') == datetime_str and a.get('status') not in ['cancelled', 'completed']:
            return True
    return False

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
<title>Medical Touch Admin Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Poppins',sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);display:flex;justify-content:center;align-items:center;min-height:100vh;}
.login-container{background:white;padding:50px;border-radius:30px;width:420px;box-shadow:0 20px 60px rgba(0,0,0,0.3);}
.login-container h1{color:#1a1a2e;font-size:28px;margin-bottom:10px;}
.login-container .sub{color:#666;margin-bottom:30px;}
.input-group{margin-bottom:20px;}
.input-group label{display:block;margin-bottom:8px;color:#333;font-weight:500;}
.input-group input{width:100%;padding:14px;border:2px solid #eee;border-radius:12px;font-size:15px;}
.input-group input:focus{outline:none;border-color:#ff6b9d;}
button{background:#ff6b9d;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:16px;font-weight:bold;cursor:pointer;transition:0.3s;}
button:hover{background:#ff4d7d;transform:scale(1.02);}
.error{color:#dc3545;margin-top:15px;text-align:center;}
.logo{font-size:50px;text-align:center;margin-bottom:20px;}
</style>
</head>
<body>
<div class="login-container">
<div class="logo">💅</div>
<h1>Medical Touch Admin</h1>
<div class="sub">Enter your credentials to access dashboard</div>
<form method="POST">
<div class="input-group"><label>Username</label><input type="text" name="username" placeholder="Enter username" required></div>
<div class="input-group"><label>Password</label><input type="password" name="password" placeholder="Enter password" required></div>
<button type="submit">Login to Dashboard</button>
</form>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
</div>
</body>
</html>
'''

CUSTOMER_HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Medical Touch | Beauty & Wellness</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Poppins',sans-serif;background:#faf8f9;}
.hero{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:80px 20px;text-align:center;position:relative;overflow:hidden;}
.hero::before{content:'💅';position:absolute;font-size:200px;opacity:0.05;bottom:-50px;right:-50px;}
.hero h1{font-family:'Playfair Display',serif;font-size:64px;letter-spacing:3px;}
.hero p{font-size:18px;opacity:0.9;margin-top:15px;}
.address{background:#ff6b9d;display:inline-block;padding:12px 35px;border-radius:50px;margin-top:25px;font-size:16px;font-weight:500;}
.search-bar{max-width:550px;margin:30px auto 0;}
.search-bar input{width:100%;padding:16px 25px;border:2px solid rgba(255,255,255,0.3);border-radius:60px;font-size:16px;background:rgba(255,255,255,0.95);transition:0.3s;}
.search-bar input:focus{outline:none;border-color:#ff6b9d;}
.tabs{display:flex;justify-content:center;gap:12px;background:white;padding:18px;box-shadow:0 4px 20px rgba(0,0,0,0.08);position:sticky;top:0;z-index:100;flex-wrap:wrap;}
.tab{padding:12px 32px;font-size:16px;font-weight:600;background:none;border:none;cursor:pointer;border-radius:50px;color:#666;transition:0.3s;}
.tab:hover{background:#ff6b9d20;color:#ff6b9d;}
.tab.active{background:#ff6b9d;color:white;box-shadow:0 4px 15px rgba(255,107,157,0.3);}
.container{max-width:1400px;margin:0 auto;padding:50px 25px;}
.tab-content{display:none;animation:fadeIn 0.4s ease;}
.tab-content.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(15px);}to{opacity:1;transform:translateY(0);}}
.category-title{font-family:'Playfair Display',serif;font-size:32px;color:#1a1a2e;margin-bottom:30px;padding-bottom:12px;border-bottom:3px solid #ff6b9d;display:inline-block;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:30px;margin-top:30px;}
.service-card{background:white;border-radius:24px;padding:25px;cursor:pointer;transition:0.3s;box-shadow:0 5px 25px rgba(0,0,0,0.05);border:1px solid #f0f0f0;}
.service-card:hover{transform:translateY(-6px);border-color:#ff6b9d;box-shadow:0 20px 35px rgba(255,107,157,0.12);}
.service-name{font-size:17px;font-weight:600;color:#1a1a2e;margin-bottom:10px;line-height:1.4;}
.service-price{font-size:28px;font-weight:bold;color:#ff6b9d;margin:12px 0 8px;}
.service-duration{color:#999;font-size:13px;display:flex;align-items:center;gap:5px;}
.service-desc{color:#888;font-size:13px;margin-top:10px;padding-top:10px;border-top:1px solid #eee;}
.book-hint{margin-top:15px;font-size:13px;color:#ff6b9d;font-weight:500;display:flex;align-items:center;gap:5px;}
.booking-section{background:linear-gradient(135deg,#fff5f7,#ffe4e8);border-radius:32px;padding:50px;margin-top:30px;}
.booking-section h2{font-family:'Playfair Display',serif;font-size:34px;color:#1a1a2e;margin-bottom:25px;}
.form-group{margin-bottom:22px;}
input,select{width:100%;padding:15px;border:2px solid #eee;border-radius:16px;font-size:15px;font-family:'Poppins',sans-serif;transition:0.3s;}
input:focus,select:focus{outline:none;border-color:#ff6b9d;}
.submit-btn{background:#ff6b9d;color:white;border:none;padding:16px;border-radius:50px;font-size:17px;font-weight:bold;cursor:pointer;width:100%;transition:0.3s;}
.submit-btn:hover{background:#ff4d7d;transform:scale(1.02);}
.warning{color:#dc3545;font-size:13px;margin-top:8px;display:none;}
footer{background:#1a1a2e;color:white;text-align:center;padding:50px;margin-top:80px;}
footer p{margin:8px 0;opacity:0.9;}
.chat-btn{position:fixed;bottom:30px;right:30px;width:70px;height:70px;background:linear-gradient(135deg,#ff6b9d,#ff4d7d);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:32px;box-shadow:0 8px 25px rgba(0,0,0,0.2);z-index:1000;transition:0.3s;}
.chat-btn:hover{transform:scale(1.1);}
.chat-window{position:fixed;bottom:120px;right:30px;width:380px;height:520px;background:white;border-radius:28px;display:none;flex-direction:column;box-shadow:0 15px 50px rgba(0,0,0,0.25);z-index:1000;overflow:hidden;}
.chat-window.show{display:flex;}
.chat-header{background:linear-gradient(135deg,#ff6b9d,#ff4d7d);color:white;padding:18px;font-weight:bold;font-size:18px;display:flex;justify-content:space-between;align-items:center;}
.chat-header button{background:none;border:none;color:white;font-size:22px;cursor:pointer;}
.chat-messages{flex:1;overflow-y:auto;padding:18px;background:#f8f9fa;}
.bot-msg{background:white;padding:12px 16px;border-radius:20px;margin:10px 0;max-width:85%;color:#333;box-shadow:0 1px 3px rgba(0,0,0,0.05);}
.user-msg{background:#ff6b9d;color:white;padding:12px 16px;border-radius:20px;margin:10px 0;max-width:85%;margin-left:auto;text-align:right;}
.quick-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:15px;}
.quick-btn{background:#f0f0f0;border:none;padding:8px 16px;border-radius:25px;font-size:12px;cursor:pointer;transition:0.3s;}
.quick-btn:hover{background:#ff6b9d;color:white;}
.chat-input{display:flex;padding:15px;border-top:1px solid #eee;background:white;}
.chat-input input{flex:1;padding:12px 18px;margin:0;margin-right:12px;border:1px solid #ddd;border-radius:30px;font-size:14px;}
.chat-input button{background:#ff6b9d;color:white;border:none;border-radius:30px;padding:12px 22px;cursor:pointer;font-weight:bold;}
.no-results{text-align:center;color:#999;padding:50px;}
@media(max-width:768px){.hero h1{font-size:36px;}.tab{padding:10px 20px;font-size:14px;}.services-grid{grid-template-columns:1fr;}.chat-window{width:320px;height:450px;right:10px;bottom:110px;}.chat-btn{bottom:20px;right:20px;}.booking-section{padding:25px;}}
</style>
</head>
<body>
<div class="hero">
<h1>MEDICAL TOUCH</h1>
<p>Where Beauty Meets Medical Excellence</p>
<div class="address">📍 Bakaata - Ain W ZEIN Road | 📞 81023625</div>
<div class="search-bar"><input type="text" id="searchInput" placeholder="🔍 Search services... (gel, lash, facial, wax)" onkeyup="searchServices()"></div>
</div>
<div class="tabs">
<button class="tab active" onclick="switchTab('nails')">💅 Nails</button>
<button class="tab" onclick="switchTab('lashes')">👁️ Lashes</button>
<button class="tab" onclick="switchTab('skincare')">💆 Skincare</button>
<button class="tab" onclick="switchTab('wax')">🕯️ Wax</button>
<button class="tab" onclick="switchTab('book')">📅 Book Now</button>
</div>
<div class="container">
<div id="nails" class="tab-content active"><div class="services-grid" id="nailsGrid"></div></div>
<div id="lashes" class="tab-content"><div class="services-grid" id="lashesGrid"></div></div>
<div id="skincare" class="tab-content"><div class="services-grid" id="skincareGrid"></div></div>
<div id="wax" class="tab-content"><div class="services-grid" id="waxGrid"></div></div>
<div id="book" class="tab-content">
<div class="booking-section">
<h2>✨ Book Your Appointment</h2>
<form id="bookingForm">
<div class="form-group"><input type="text" id="custName" placeholder="Full Name *" required></div>
<div class="form-group"><input type="tel" id="custPhone" placeholder="Phone Number *" required></div>
<div class="form-group"><input type="email" id="custEmail" placeholder="Email (optional)"></div>
<div class="form-group"><select id="serviceSelect" required><option value="">Select a Service</option></select></div>
<div class="form-group"><input type="datetime-local" id="appointmentDate" required></div>
<div id="slotWarning" class="warning">⚠️ This time slot is already booked. Please choose another time.</div>
<button type="submit" class="submit-btn">Confirm Booking</button>
</form>
</div>
</div>
</div>
<footer>
<p>✨ Medical Touch - Where Beauty Meets Medical Excellence ✨</p>
<p>📍 Bakaata - Ain W ZEIN Road | 📞 81023625</p>
<p>⏰ Open Daily: 10:00 AM - 8:00 PM</p>
</footer>
<div class="chat-btn" onclick="toggleChat()">💬</div>
<div class="chat-window" id="chatWindow">
<div class="chat-header">🤖 Medical Touch AI Assistant <button onclick="toggleChat()">✕</button></div>
<div class="chat-messages" id="chatMsgs">
<div class="bot-msg">Hello! 👋 I'm your beauty assistant. Ask me about nails, lashes, skincare, wax, or prices! Click a button below for quick answers.</div>
<div class="quick-btns">
<button class="quick-btn" onclick="sendQuick('nails')">💅 Nail Services</button>
<button class="quick-btn" onclick="sendQuick('lashes')">👁️ Lash Services</button>
<button class="quick-btn" onclick="sendQuick('skincare')">💆 Skincare & Meso</button>
<button class="quick-btn" onclick="sendQuick('wax')">🕯️ Wax Services</button>
<button class="quick-btn" onclick="sendQuick('prices')">💰 Price List</button>
<button class="quick-btn" onclick="sendQuick('booking')">📅 How to Book</button>
<button class="quick-btn" onclick="sendQuick('location')">📍 Location & Hours</button>
</div>
</div>
<div class="chat-input">
<input type="text" id="chatInput" placeholder="Type your question here..." onkeypress="if(event.key==='Enter')sendChat()">
<button onclick="sendChat()">Send</button>
</div>
</div>
<script>
let allServices = [];
fetch('/api/services').then(r=>r.json()).then(services => {
allServices = services;
displayServices(services);
populateSelect(services);
});
function displayServices(services){
const cats = {'Nails':'nailsGrid','Lashes':'lashesGrid','Skincare':'skincareGrid','Wax':'waxGrid'};
for(let [cat, elId] of Object.entries(cats)){
let filtered = services.filter(s => s.category === cat);
let html = '';
filtered.forEach(s => {
html += `<div class="service-card" onclick="bookService('${s.name.replace(/'/g, "\\'")}')">
<div class="service-name">${s.name}</div>
<div class="service-price">$${s.price}</div>
<div class="service-duration">⏱️ ${s.duration} minutes</div>
<div class="service-desc">${s.description || 'Professional service'}</div>
<div class="book-hint">✨ Click to book →</div>
</div>`;
});
document.getElementById(elId).innerHTML = html || '<p class="no-results">No services found in this category</p>';
}}
function searchServices(){
const term = document.getElementById('searchInput').value.toLowerCase();
const cats = ['nails','lashes','skincare','wax'];
for(let cat of cats){
const grid = document.getElementById(cat+'Grid');
const cards = grid.querySelectorAll('.service-card');
cards.forEach(card => {
const name = card.querySelector('.service-name').innerText.toLowerCase();
card.style.display = (term === '' || name.includes(term)) ? 'block' : 'none';
});
}
}
function populateSelect(services){
let html = '<option value="">Select a Service</option>';
services.forEach(s => { html += `<option value="${s.name.replace(/'/g, "\\'")}">${s.name} - $${s.price} (${s.duration} min)</option>`; });
document.getElementById('serviceSelect').innerHTML = html;
}
function bookService(name){
document.getElementById('serviceSelect').value = name;
switchTab('book');
}
function switchTab(tab){
document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
event.target.classList.add('active');
document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
document.getElementById(tab).classList.add('active');
}
document.getElementById('appointmentDate').onchange = async function() {
const res = await fetch('/api/check-slot', {
method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({datetime:this.value})
});
const data = await res.json();
document.getElementById('slotWarning').style.display = data.booked ? 'block' : 'none';
};
document.getElementById('bookingForm').onsubmit = async (e) => {
e.preventDefault();
const data = {
name: document.getElementById('custName').value,
phone: document.getElementById('custPhone').value,
email: document.getElementById('custEmail').value,
service: document.getElementById('serviceSelect').value,
datetime: document.getElementById('appointmentDate').value
};
if(!data.name || !data.phone || !data.service || !data.datetime){
alert('Please fill all required fields');
return;
}
const res = await fetch('/api/customer-book', {
method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify(data)
});
const result = await res.json();
if(result.success) alert('✅ Appointment booked successfully! We will confirm via SMS.');
else if(result.double_booking) alert('❌ Sorry, this time is already taken. Please choose another time.');
else alert('❌ An error occurred. Please try again.');
if(result.success) document.getElementById('bookingForm').reset();
};
function toggleChat(){document.getElementById('chatWindow').classList.toggle('show');}
async function sendChat(){
const input = document.getElementById('chatInput');
const q = input.value.trim();
if(!q) return;
const msgs = document.getElementById('chatMsgs');
msgs.innerHTML += `<div class="user-msg">${q}</div>`;
input.value = '';
const res = await fetch('/api/ai/customer-chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
const data = await res.json();
msgs.innerHTML += `<div class="bot-msg">${data.answer}</div>`;
msgs.scrollTop = msgs.scrollHeight;
}
async function sendQuick(topic){
let q = '';
if(topic === 'nails') q = 'Tell me about your nail services';
else if(topic === 'lashes') q = 'Tell me about your lash services';
else if(topic === 'skincare') q = 'Tell me about your skincare and mesotherapy treatments';
else if(topic === 'wax') q = 'Tell me about your wax services';
else if(topic === 'prices') q = 'What are your price ranges for all services?';
else if(topic === 'booking') q = 'How do I book an appointment?';
else if(topic === 'location') q = 'Where are you located and what are your hours?';
const msgs = document.getElementById('chatMsgs');
msgs.innerHTML += `<div class="user-msg">${q}</div>`;
const res = await fetch('/api/ai/customer-chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
const data = await res.json();
msgs.innerHTML += `<div class="bot-msg">${data.answer}</div>`;
msgs.scrollTop = msgs.scrollHeight;
}
</script>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Medical Touch | Admin Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Poppins',sans-serif;background:#f0f2f5;}
.sidebar{width:280px;background:linear-gradient(180deg,#1a1a2e,#16213e);color:white;position:fixed;height:100%;padding:30px 20px;overflow-y:auto;}
.sidebar h2{font-size:24px;margin-bottom:45px;text-align:center;}
.sidebar nav a{display:block;color:white;text-decoration:none;padding:14px 20px;margin:10px 0;border-radius:14px;transition:0.3s;cursor:pointer;font-weight:500;}
.sidebar nav a:hover{background:#ff6b9d;transform:translateX(8px);}
.main{margin-left:280px;padding:30px;}
.top-bar{background:white;padding:20px 30px;border-radius:20px;margin-bottom:30px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 15px rgba(0,0,0,0.05);}
.top-bar h2{color:#1a1a2e;}
.logout-btn{background:#ff4d7d;color:white;border:none;padding:12px 28px;border-radius:40px;cursor:pointer;font-weight:600;transition:0.3s;}
.logout-btn:hover{background:#dc3545;transform:scale(1.02);}
.wheels-container{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:35px;}
.wheel-card{background:white;border-radius:24px;padding:30px;text-align:center;box-shadow:0 5px 20px rgba(0,0,0,0.05);}
.wheel-card h3{color:#1a1a2e;margin-bottom:25px;font-size:20px;}
.wheel{display:flex;justify-content:center;gap:25px;flex-wrap:wrap;}
.wheel-item{width:120px;height:120px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;cursor:pointer;transition:0.3s;}
.wheel-item:hover{transform:scale(1.08);}
.wheel-item span{font-size:26px;font-weight:bold;}
.wheel-item div{font-size:13px;margin-top:6px;}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:25px;margin-bottom:35px;}
.stat-card{background:white;border-radius:20px;padding:25px;text-align:center;box-shadow:0 5px 20px rgba(0,0,0,0.05);}
.stat-card .number{font-size:38px;font-weight:bold;color:#ff6b9d;}
.stat-card p{color:#666;font-size:14px;margin-top:10px;}
.section{background:white;border-radius:24px;padding:30px;margin-bottom:30px;display:none;box-shadow:0 5px 20px rgba(0,0,0,0.05);}
.section.active{display:block;}
.section h2{color:#1a1a2e;margin-bottom:25px;font-size:24px;}
table{width:100%;border-collapse:collapse;}
th,td{padding:14px;text-align:left;border-bottom:1px solid #eee;}
th{background:#fef8f9;color:#ff6b9d;font-weight:600;}
.delete-btn{background:#dc3545;color:white;border:none;padding:6px 14px;border-radius:8px;cursor:pointer;}
.edit-btn{background:#ffc107;color:#333;border:none;padding:6px 14px;border-radius:8px;cursor:pointer;}
input,select{padding:10px;margin:5px;border:1px solid #ddd;border-radius:10px;}
button{background:#ff6b9d;color:white;border:none;padding:12px 24px;border-radius:12px;cursor:pointer;font-weight:500;transition:0.3s;}
button:hover{transform:scale(1.02);}
.profit-detail{margin-top:20px;padding:18px;background:#fef8f9;border-radius:14px;display:none;font-size:14px;line-height:1.6;}
.ai-box{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:24px;padding:35px;color:white;}
.ai-box input{width:70%;padding:14px;border:none;border-radius:40px;margin-right:12px;}
.ai-box button{background:white;color:#764ba2;border:none;padding:14px 30px;border-radius:40px;cursor:pointer;font-weight:bold;}
.ai-response{margin-top:25px;padding:18px;background:rgba(255,255,255,0.2);border-radius:16px;display:none;line-height:1.5;}
.appointment-tabs{display:flex;gap:15px;margin-bottom:25px;border-bottom:2px solid #eee;flex-wrap:wrap;}
.appt-tab{padding:12px 28px;cursor:pointer;border:none;background:none;font-weight:600;border-radius:40px;transition:0.3s;}
.appt-tab:hover{background:#f0f0f0;}
.appt-tab.active{background:#ff6b9d;color:white;}
.appointment-list{display:none;}
.appointment-list.active{display:block;}
.appt-card{padding:18px;margin:12px 0;border-radius:16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:15px;}
.status-pending{background:linear-gradient(135deg,#fff5f5,#ffe0e0);border-left:5px solid #dc3545;}
.status-confirmed{background:linear-gradient(135deg,#f0fff4,#d4f5e0);border-left:5px solid #28a745;}
.status-completed{background:linear-gradient(135deg,#e8f4fd,#d0e8f5);border-left:5px solid #007bff;}
.status-cancelled{background:#f8f9fa;border-left:5px solid #6c757d;opacity:0.8;}
.appt-info{flex:1;}
.appt-actions{display:flex;gap:10px;flex-wrap:wrap;}
.btn-confirm{background:#28a745;color:white;border:none;padding:8px 16px;border-radius:10px;cursor:pointer;font-weight:500;}
.btn-complete{background:#007bff;color:white;border:none;padding:8px 16px;border-radius:10px;cursor:pointer;font-weight:500;}
.btn-cancel{background:#ffc107;color:#333;border:none;padding:8px 16px;border-radius:10px;cursor:pointer;font-weight:500;}
.btn-delete{background:#dc3545;color:white;border:none;padding:8px 16px;border-radius:10px;cursor:pointer;font-weight:500;}
.notes-input{width:100%;padding:10px;margin-top:8px;border:1px solid #ddd;border-radius:10px;font-size:13px;}
.floating-bell{position:fixed;bottom:30px;right:30px;width:65px;height:65px;background:linear-gradient(135deg,#ff6b9d,#ff4d7d);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:30px;box-shadow:0 8px 25px rgba(0,0,0,0.15);z-index:1000;transition:0.3s;}
.floating-bell:hover{transform:scale(1.08);}
.bell-badge{position:absolute;top:-6px;right:-6px;background:#dc3545;color:white;border-radius:50%;width:24px;height:24px;font-size:12px;display:flex;align-items:center;justify-content:center;}
.notif-popup{position:fixed;bottom:115px;right:30px;width:350px;background:white;border-radius:20px;display:none;box-shadow:0 15px 40px rgba(0,0,0,0.2);z-index:1000;}
.notif-popup.show{display:block;}
.notif-header{background:#ff6b9d;color:white;padding:15px;border-radius:20px 20px 0 0;font-weight:bold;}
.notif-list{max-height:380px;overflow-y:auto;}
.notif-item{padding:14px;border-bottom:1px solid #eee;font-size:13px;}
.notif-time{font-size:10px;color:#999;margin-top:6px;}
@media(max-width:768px){.sidebar{width:100%;height:auto;position:relative;}.main{margin-left:0;}.wheels-container{grid-template-columns:1fr;}.stats-grid{grid-template-columns:1fr 1fr;}}
</style>
</head>
<body>
<div class="sidebar">
<h2>💅 MEDICAL TOUCH</h2>
<nav>
<a onclick="showSection('dashboard')">📊 Dashboard</a>
<a onclick="showSection('customers')">👥 Customers</a>
<a onclick="showSection('appointments')">📅 Appointments</a>
<a onclick="showSection('services')">💅 Services</a>
<a onclick="showSection('materials')">📦 Materials & Costs</a>
<a onclick="showSection('ai')">🤖 AI Assistant</a>
</nav>
</div>
<div class="main">
<div class="top-bar">
<h2>✨ Admin Dashboard ✨</h2>
<button class="logout-btn" onclick="location.href='/admin/logout'">🚪 Logout</button>
</div>
<div id="dashboard" class="section active">
<div class="wheels-container">
<div class="wheel-card">
<h3>💰 Profit Wheels (Click to view)</h3>
<div class="wheel">
<div class="wheel-item" style="background:#1a1a2e;" onclick="showProfit('today')"><span id="todayAmt">$0</span><div>Today</div></div>
<div class="wheel-item" style="background:#ff6b9d;" onclick="showProfit('week')"><span id="weekAmt">$0</span><div>This Week</div></div>
<div class="wheel-item" style="background:#ff4d7d;" onclick="showProfit('month')"><span id="monthAmt">$0</span><div>This Month</div></div>
<div class="wheel-item" style="background:#1a1a2e;" onclick="showProfit('year')"><span id="yearAmt">$0</span><div>This Year</div></div>
</div>
<div id="profitDetail" class="profit-detail"></div>
</div>
<div class="wheel-card">
<h3>🎯 Most Wanted Services</h3>
<div class="wheel" id="popularWheel"></div>
<div id="popularDetail" class="profit-detail"></div>
</div>
</div>
<div class="stats-grid" id="statsGrid"></div>
<h3 style="margin:20px 0 15px 0;">📋 Recent Bookings</h3>
<div id="recentList"></div>
</div>
<div id="customers" class="section">
<h2>👥 Customer Directory</h2>
<div id="customerTable"></div>
</div>
<div id="appointments" class="section">
<h2>📅 Appointment Manager</h2>
<div class="appointment-tabs">
<button class="appt-tab active" onclick="filterAppointments('pending')">⏳ Pending (<span id="pendingCount">0</span>)</button>
<button class="appt-tab" onclick="filterAppointments('confirmed')">✅ Confirmed (<span id="confirmedCount">0</span>)</button>
<button class="appt-tab" onclick="filterAppointments('completed')">⭐ Completed (<span id="completedCount">0</span>)</button>
<button class="appt-tab" onclick="filterAppointments('cancelled')">❌ Cancelled (<span id="cancelledCount">0</span>)</button>
</div>
<div id="pendingList" class="appointment-list active"></div>
<div id="confirmedList" class="appointment-list"></div>
<div id="completedList" class="appointment-list"></div>
<div id="cancelledList" class="appointment-list"></div>
</div>
<div id="services" class="section">
<h2>💅 Service Manager</h2>
<div style="margin-bottom:25px;display:flex;flex-wrap:wrap;gap:12px;">
<input type="text" id="newName" placeholder="Service Name" style="width:220px;">
<input type="number" id="newPrice" placeholder="Price $" style="width:100px;">
<select id="newCat" style="width:130px;">
<option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option>
</select>
<input type="number" id="newCost" placeholder="Material Cost $" style="width:130px;">
<button onclick="addService()">➕ Add Service</button>
</div>
<div id="serviceTable"></div>
</div>
<div id="materials" class="section">
<h2>📦 Materials & Monthly Costs</h2>
<div id="materialsGrid"></div>
<div id="profitSummary" style="margin-top:25px;padding:25px;background:#fef8f9;border-radius:18px;"></div>
</div>
<div id="ai" class="section">
<div class="ai-box">
<h2>🤖 AI Business Assistant</h2>
<p>Ask me anything about profits, popular services, predictions, or growth strategies!</p>
<div style="margin-top:25px;">
<input type="text" id="aiQuestion" placeholder="e.g., How much profit after materials?">
<button onclick="askAI()">Ask AI</button>
</div>
<div id="aiResponse" class="ai-response"></div>
</div>
</div>
</div>
<div class="floating-bell" onclick="toggleNotif()">
🔔
<span id="bellBadge" class="bell-badge" style="display:none;">0</span>
</div>
<div id="notifPopup" class="notif-popup">
<div class="notif-header">🔔 Real-Time Notifications</div>
<div id="notifList" class="notif-list"></div>
</div>
<script>
let profitData = {};
let popularData = [];
function showSection(s){
document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
document.getElementById(s).classList.add('active');
if(s==='dashboard') loadDashboard();
if(s==='customers') loadCustomers();
if(s==='appointments') loadAppointments();
if(s==='services') loadServices();
if(s==='materials') loadMaterials();
}
async function loadDashboard(){
const r = await fetch('/api/admin/stats');
const d = await r.json();
profitData = d.profit;
popularData = d.popular;
document.getElementById('todayAmt').innerText = '$'+profitData.today;
document.getElementById('weekAmt').innerText = '$'+profitData.week;
document.getElementById('monthAmt').innerText = '$'+profitData.month;
document.getElementById('yearAmt').innerText = '$'+profitData.year;
let statsHtml = '';
d.stats.forEach(s => { statsHtml += `<div class="stat-card"><div class="number">${s.value}</div><p>${s.title}</p></div>`; });
document.getElementById('statsGrid').innerHTML = statsHtml;
let popularHtml = '';
const colors = ['#ff6b9d','#ff4d7d','#ffb347','#4ecdc4','#45b7d1','#96ceb4'];
popularData.forEach((p,i) => {
popularHtml += `<div class="wheel-item" style="background:${colors[i%colors.length]}" onclick="showPopular('${p.name.replace(/'/g, "\\'")}')"><span>${p.name.substring(0,8)}</span><div>${p.count} 📅</div><div style="font-size:11px;margin-top:3px;">💰 $${p.revenue}</div></div>`;
});
document.getElementById('popularWheel').innerHTML = popularHtml || '<p style="text-align:center;">No service data yet</p>';
let recentHtml = '';
d.recent.forEach(a => {
let statusClass = '';
if(a.status==='pending') statusClass = 'status-pending';
else if(a.status==='confirmed') statusClass = 'status-confirmed';
else if(a.status==='completed') statusClass = 'status-completed';
else statusClass = 'status-cancelled';
recentHtml += `<div class="${statusClass} appt-card"><div class="appt-info"><strong>${a.customer_name}</strong> - ${a.service}<br>📅 ${a.datetime}<br>Status: ${a.status}</div></div>`;
});
document.getElementById('recentList').innerHTML = recentHtml || '<p>No appointments yet</p>';
}
function showProfit(p){
const d = document.getElementById('profitDetail');
let msg = '';
if(p==='today') msg = '💰 Today: $'+profitData.today+' ('+(profitData.todayCount||0)+' appointments) | Net Profit: $'+(profitData.todayNet||0);
if(p==='week') msg = '💰 This Week: $'+profitData.week+' ('+(profitData.weekCount||0)+' appointments) | Net Profit: $'+(profitData.weekNet||0);
if(p==='month') msg = '💰 This Month: $'+profitData.month+' ('+(profitData.monthCount||0)+' appointments) | Net Profit: $'+(profitData.monthNet||0);
if(p==='year') msg = '💰 This Year: $'+profitData.year+' ('+(profitData.yearCount||0)+' appointments) | Net Profit: $'+(profitData.yearNet||0);
d.innerHTML = msg;
d.style.display = 'block';
setTimeout(()=>d.style.display='none',5000);
}
function showPopular(n){
const d = document.getElementById('popularDetail');
const p = popularData.find(x => x.name === n);
if(p) d.innerHTML = '🎯 '+p.name+': '+p.count+' bookings | Revenue: $'+p.revenue+' | Material Cost: $'+p.materialCost+' | Net Profit: $'+p.netProfit;
d.style.display = 'block';
setTimeout(()=>d.style.display='none',5000);
}
async function loadCustomers(){
const r = await fetch('/api/customers');
const c = await r.json();
let h = '<table><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Notes</th><th>Action</th></tr>';
c.forEach(cust => { h += `<tr>
<td>${cust.name}</td>
<td>${cust.phone}</td>
<td>${cust.email || '-'}</td>
<td>${cust.visits || 0}</td>
<td><input class="notes-input" type="text" id="note_${cust.id}" value="${cust.notes || ''}" placeholder="Add notes..."></td>
<td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button> <button onclick="saveNote('${cust.id}')">Save Note</button></td>
</table>`; });
h += '</table>';
document.getElementById('customerTable').innerHTML = h;
}
async function saveNote(id){
const note = document.getElementById('note_'+id).value;
await fetch('/api/customers/'+id+'/note',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({notes:note})});
alert('✅ Note saved successfully!');
}
async function loadAppointments(){
const r = await fetch('/api/appointments');
const a = await r.json();
let pending = '', confirmed = '', completed = '', cancelled = '';
let pendingCt = 0, confirmedCt = 0, completedCt = 0, cancelledCt = 0;
a.forEach(app => {
const actions = `<div class="appt-actions">
${app.status==='pending' ? `<button class="btn-confirm" onclick="updateStatus('${app.id}','confirmed')">✅ Confirm</button>` : ''}
${app.status==='pending' || app.status==='confirmed' ? `<button class="btn-complete" onclick="updateStatus('${app.id}','completed')">⭐ Complete</button>` : ''}
<button class="btn-cancel" onclick="cancelAppointment('${app.id}')">❌ Cancel</button>
<button class="btn-delete" onclick="deleteAppointment('${app.id}')">🗑️ Delete</button>
</div>`;
const card = `<div class="status-${app.status} appt-card">
<div class="appt-info"><strong>${app.customer_name}</strong> - ${app.service}<br>📅 ${app.datetime}<br>Status: ${app.status}</div>
${actions}
</div>`;
if(app.status==='pending') { pending += card; pendingCt++; }
else if(app.status==='confirmed') { confirmed += card; confirmedCt++; }
else if(app.status==='completed') { completed += card; completedCt++; }
else if(app.status==='cancelled') { cancelled += card; cancelledCt++; }
});
document.getElementById('pendingList').innerHTML = pending || '<p style="padding:20px;text-align:center;">No pending appointments</p>';
document.getElementById('confirmedList').innerHTML = confirmed || '<p style="padding:20px;text-align:center;">No confirmed appointments</p>';
document.getElementById('completedList').innerHTML = completed || '<p style="padding:20px;text-align:center;">No completed appointments</p>';
document.getElementById('cancelledList').innerHTML = cancelled || '<p style="padding:20px;text-align:center;">No cancelled appointments</p>';
document.getElementById('pendingCount').innerText = pendingCt;
document.getElementById('confirmedCount').innerText = confirmedCt;
document.getElementById('completedCount').innerText = completedCt;
document.getElementById('cancelledCount').innerText = cancelledCt;
}
async function updateStatus(id,status){
await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:status})});
loadAppointments();
loadDashboard();
}
async function cancelAppointment(id){
if(confirm('Cancel this appointment?')){
await fetch('/api/appointments/'+id+'/cancel',{method:'PUT'});
loadAppointments();
loadDashboard();
}
}
async function deleteAppointment(id){
if(confirm('Permanently delete this appointment?')){
await fetch('/api/appointments/'+id,{method:'DELETE'});
loadAppointments();
loadDashboard();
}
}
function filterAppointments(status){
document.querySelectorAll('.appt-tab').forEach(t=>t.classList.remove('active'));
event.target.classList.add('active');
document.querySelectorAll('.appointment-list').forEach(list=>list.classList.remove('active'));
document.getElementById(status+'List').classList.add('active');
}
async function loadServices(){
const r = await fetch('/api/services');
const s = await r.json();
let h = '<table><th>Name</th><th>Price</th><th>Duration</th><th>Category</th><th>Material</th><th>Action</th></tr>';
s.forEach(serv => { h += `<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.duration}min</td><td>${serv.category}</td><td>$${serv.material_cost||0}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td>`; });
h += '</table>';
document.getElementById('serviceTable').innerHTML = h;
}
async function addService(){
await fetch('/api/services',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
name:document.getElementById('newName').value,
price:parseInt(document.getElementById('newPrice').value),
duration:60,
category:document.getElementById('newCat').value,
material_cost:parseInt(document.getElementById('newCost').value)||0
})});
loadServices();
document.getElementById('newName').value='';
document.getElementById('newPrice').value='';
document.getElementById('newCost').value='';
alert('✅ Service added successfully!');
}
async function deleteService(id){ if(confirm('Delete this service?')){ await fetch('/api/services/'+id,{method:'DELETE'}); loadServices(); } }
async function deleteCustomer(id){ if(confirm('Delete this customer? This will also delete their appointment history.')){ await fetch('/api/customers/'+id,{method:'DELETE'}); loadCustomers(); loadDashboard(); } }
async function loadMaterials(){
const r = await fetch('/api/materials');
const d = await r.json();
let h = '<table><th>Category</th><th>Monthly Cost</th><th>Items</th><th>Action</th></tr>';
for(let cat in d.materials){
h += `<tr><td><strong>${cat}</strong></td><td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:90px;"> $</td><td>${d.materials[cat].items.join(', ')}</td><td><button onclick="updateCost('${cat}')">Update</button></td>`; }
h += '</table>';
document.getElementById('materialsGrid').innerHTML = h;
document.getElementById('profitSummary').innerHTML = `<h3>💰 Financial Summary</h3><p>Total Revenue: $${d.totalRevenue} | Total Material Cost: $${d.totalMaterialCost} | <strong style="color:#28a745;">Net Profit: $${d.netProfit}</strong></p><p>Profit Margin: ${((d.netProfit/d.totalRevenue)*100).toFixed(1)}%</p>`;
}
async function updateCost(cat){
const cost = document.getElementById('cost_'+cat).value;
await fetch('/api/materials/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat,cost:parseInt(cost)})});
loadMaterials();
alert('✅ Cost updated!');
}
async function askAI(){
const q = document.getElementById('aiQuestion').value;
if(!q) return;
const r = await fetch('/api/ai/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
const d = await r.json();
document.getElementById('aiResponse').innerHTML = d.answer;
document.getElementById('aiResponse').style.display = 'block';
}
let lastCount = 0;
async function loadNotif(){
const r = await fetch('/api/notifications');
const n = await r.json();
const b = document.getElementById('bellBadge');
if(n.length>0){ b.style.display='flex'; b.innerText=n.length; } else { b.style.display='none'; }
let h = '';
n.forEach(not => { h += `<div class="notif-item">🔔 ${not.message}<div class="notif-time">${not.time}</div></div>`; });
document.getElementById('notifList').innerHTML = h || '<div style="padding:15px;text-align:center;">No notifications</div>';
if(n.length>lastCount && lastCount>0){ document.querySelector('.floating-bell').style.transform='scale(1.15)'; setTimeout(()=>document.querySelector('.floating-bell').style.transform='scale(1)',300); }
lastCount = n.length;
}
function toggleNotif(){ const p = document.getElementById('notifPopup'); p.classList.toggle('show'); if(p.classList.contains('show')) loadNotif(); }
loadDashboard(); loadNotif(); setInterval(()=>{ if(document.getElementById('dashboard').classList.contains('active')) loadDashboard(); loadNotif(); },15000);
</script>
</body>
</html>
'''

# API ROUTES
@app.route('/')
def customer_site():
    return render_template_string(CUSTOMER_HTML)

@app.route('/admin')
def admin_login_page():
    if session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))
    return render_template_string(LOGIN_PAGE)

@app.route('/admin', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template_string(LOGIN_PAGE, error='Invalid credentials')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template_string(ADMIN_HTML)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login_page'))

@app.route('/api/ai/customer-chat', methods=['POST'])
def customer_chat():
    q = request.json.get('question', '').lower()
    if 'nail' in q or 'manicure' in q or 'pedicure' in q:
        a = "💅 **Our Nail Services:**\n• Gel Manicure: $35\n• Acrylic Full Set: $40\n• Dipping Powder: $30\n• Manicure: $10\n• Pedicure: $15\n• Nail Art: $15\n• Paraffin Treatment: $8\n\nAll services include professional care and long-lasting results! Book now via the Book tab."
    elif 'lash' in q or 'lashes' in q:
        a = "👁️ **Our Lash Services:**\n• Classic Lashes: $35 (natural look)\n• Volume Lashes: $38 (fluffy fullness)\n• Mega Volume: $45 (dramatic effect)\n• Refill: $25\n• Removal: $20\n\nLasts 3-4 weeks with proper care! Book your appointment today."
    elif 'skin' in q or 'facial' in q or 'meso' in q or 'skincare' in q:
        a = "💆 **Our Skincare & Mesotherapy:**\n• Classic Facial: $35\n• HydraFacial: $55\n• Medical Facial + Meso: $65\n• HIFU Lifting: $100\n• MesoPen treatments: $35-100\n• Meso Injections: $100-200\n\nResults guaranteed! Book a consultation to find your perfect treatment."
    elif 'wax' in q:
        a = "🕯️ **Our Wax Services:**\n• Full Body: $45\n• Full Legs: $17\n• Bikini: $23\n• Underarms: $6\n• Full Arms: $12\n• Back/Chest: $18\n• Eyebrows: $4-6\n• Lips: $3-5\n\nPain-free with our premium wax! Walk-ins welcome."
    elif 'price' in q or 'cost' in q or 'prices' in q:
        a = "💰 **Medical Touch Price Range:**\n\n💅 **Nails:** $10-40\n👁️ **Lashes:** $35-45\n💆 **Skincare:** $35-200\n🕯️ **Wax:** $3-45\n\nVisit our website for complete price list or call 81023625 for custom packages!"
    elif 'book' in q or 'appointment' in q:
        a = "📅 **How to Book:**\n\n1. Go to the 'Book Now' tab\n2. Select your desired service\n3. Choose your preferred date and time\n4. Enter your details\n5. Click 'Confirm Booking'\n\nYou'll receive SMS confirmation within minutes! Or call us at 81023625 for phone booking."
    elif 'location' in q or 'address' in q or 'where' in q or 'hour' in q:
        a = "📍 **Medical Touch Location & Hours:**\n\nAddress: Bakaata - Ain W ZEIN Road\n\n⏰ **Open Daily:** 10:00 AM - 8:00 PM\n📞 **Phone:** 81023625\n\nFree parking available! We're located in the heart of Bakaata."
    else:
        a = "✨ **Medical Touch Beauty & Wellness** ✨\n\nWe specialize in:\n• 💅 Professional Nail Services\n• 👁️ Premium Lash Extensions\n• 💆 Advanced Skincare & Mesotherapy\n• 🕯️ Gentle Waxing\n\nAsk me about any service, prices, booking, location, or hours! Or click the quick buttons above for instant answers.\n\n📞 Call us: 81023625"
    return jsonify({'answer': a})

@app.route('/api/services', methods=['GET'])
def get_services():
    data = load_data()
    return jsonify(data['services'])

@app.route('/api/services', methods=['POST'])
def add_service():
    data = load_data()
    new = request.json
    new['id'] = str(len(data['services']) + 1)
    data['services'].append(new)
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    data = load_data()
    data['services'] = [s for s in data['services'] if s['id'] != service_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/check-slot', methods=['POST'])
def check_slot():
    return jsonify({'booked': check_double_booking('staff1', request.json['datetime'])})

@app.route('/api/customer-book', methods=['POST'])
def customer_book():
    data = load_data()
    b = request.json
    if check_double_booking('staff1', b['datetime']):
        return jsonify({'success': False, 'double_booking': True})
    cust = next((c for c in data['customers'] if c['phone'] == b['phone']), None)
    if not cust:
        cust = {'id': str(len(data['customers']) + 1), 'name': b['name'], 'phone': b['phone'], 'email': b.get('email', ''), 'visits': 0, 'notes': ''}
        data['customers'].append(cust)
    appt = {'id': str(len(data['appointments']) + 1), 'customer_id': cust['id'], 'customer_name': cust['name'], 'service': b['service'], 'datetime': b['datetime'], 'status': 'pending', 'staff_id': 'staff1', 'booked_at': datetime.now().isoformat()}
    data['appointments'].append(appt)
    save_data(data)
    add_notification(f"📅 NEW BOOKING: {cust['name']} booked {b['service']} on {b['datetime']}")
    return jsonify({'success': True})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(load_data()['customers'])

@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    data = load_data()
    data['customers'] = [c for c in data['customers'] if c['id'] != customer_id]
    data['appointments'] = [a for a in data['appointments'] if a['customer_id'] != customer_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/customers/<customer_id>/note', methods=['PUT'])
def update_customer_note(customer_id):
    data = load_data()
    note = request.json.get('notes', '')
    for c in data['customers']:
        if c['id'] == customer_id:
            c['notes'] = note
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    return jsonify(load_data()['appointments'])

@app.route('/api/appointments/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    data = load_data()
    data['appointments'] = [a for a in data['appointments'] if a['id'] != appointment_id]
    save_data(data)
    add_notification(f"🗑️ Appointment #{appointment_id} was deleted")
    return jsonify({'success': True})

@app.route('/api/appointments/<appointment_id>/cancel', methods=['PUT'])
def cancel_appointment(appointment_id):
    data = load_data()
    for a in data['appointments']:
        if a['id'] == appointment_id:
            a['status'] = 'cancelled'
            add_notification(f"❌ CANCELLED: {a['customer_name']} - {a['service']}")
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/appointments/<appointment_id>/status', methods=['PUT'])
def update_status_api(appointment_id):
    data = load_data()
    status = request.json.get('status')
    for a in data['appointments']:
        if a['id'] == appointment_id:
            a['status'] = status
            if status == 'completed':
                cust = next((c for c in data['customers'] if c['id'] == a['customer_id']), None)
                if cust:
                    cust['visits'] = cust.get('visits', 0) + 1
                add_notification(f"✅ COMPLETED: {a['customer_name']} - {a['service']}")
            elif status == 'confirmed':
                add_notification(f"📌 CONFIRMED: {a['customer_name']} - {a['service']}")
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/materials', methods=['GET'])
def get_materials():
    data = load_data()
    services = {s['name']: s for s in data['services']}
    apps = data['appointments']
    rev = 0
    mat = 0
    for a in apps:
        if a.get('status') == 'completed':
            s = services.get(a['service'])
            if s:
                rev += s['price']
                mat += s.get('material_cost', 0)
    return jsonify({'materials': data.get('materials', {}), 'totalRevenue': rev, 'totalMaterialCost': mat, 'netProfit': rev - mat})

@app.route('/api/materials/update', methods=['POST'])
def update_materials():
    data = load_data()
    req = request.json
    data['materials'][req['category']]['cost'] = req['cost']
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    return jsonify(load_notifications())

@app.route('/api/admin/stats', methods=['GET'])
@login_required
def admin_stats():
    data = load_data()
    apps = data['appointments']
    services = {s['name']: {'price': s['price'], 'material_cost': s.get('material_cost', 0)} for s in data['services']}
    today = datetime.now().strftime('%Y-%m-%d')
    week = datetime.now().isocalendar()[1]
    month = datetime.now().month
    year = datetime.now().year
    t_rev = w_rev = m_rev = y_rev = 0
    t_mat = w_mat = m_mat = y_mat = 0
    t_cnt = w_cnt = m_cnt = y_cnt = 0
    pop = {}
    pop_rev = {}
    pop_mat = {}
    for a in apps:
        if a.get('status') == 'completed':
            s = services.get(a['service'])
            if s:
                pop[a['service']] = pop.get(a['service'], 0) + 1
                pop_rev[a['service']] = pop_rev.get(a['service'], 0) + s['price']
                pop_mat[a['service']] = pop_mat.get(a['service'], 0) + s['material_cost']
                try:
                    d = datetime.fromisoformat(a['datetime'])
                    if d.strftime('%Y-%m-%d') == today:
                        t_rev += s['price']; t_mat += s['material_cost']; t_cnt += 1
                    if d.isocalendar()[1] == week and d.year == year:
                        w_rev += s['price']; w_mat += s['material_cost']; w_cnt += 1
                    if d.month == month and d.year == year:
                        m_rev += s['price']; m_mat += s['material_cost']; m_cnt += 1
                    if d.year == year:
                        y_rev += s['price']; y_mat += s['material_cost']; y_cnt += 1
                except:
                    pass
    popular = []
    for name in pop:
        popular.append({
            'name': name,
            'count': pop[name],
            'revenue': pop_rev.get(name, 0),
            'materialCost': pop_mat.get(name, 0),
            'netProfit': pop_rev.get(name, 0) - pop_mat.get(name, 0)
        })
    popular.sort(key=lambda x: x['count'], reverse=True)
    popular = popular[:6]
    return jsonify({
        'profit': {
            'today': t_rev, 'week': w_rev, 'month': m_rev, 'year': y_rev,
            'todayNet': t_rev - t_mat, 'weekNet': w_rev - w_mat,
            'monthNet': m_rev - m_mat, 'yearNet': y_rev - y_mat,
            'todayCount': t_cnt, 'weekCount': w_cnt, 'monthCount': m_cnt, 'yearCount': y_cnt
        },
        'stats': [
            {'title': '👥 Total Customers', 'value': len(data['customers'])},
            {'title': '📅 Total Appointments', 'value': len(apps)},
            {'title': '⏳ Pending', 'value': sum(1 for a in apps if a.get('status') == 'pending')},
            {'title': '✅ Completed', 'value': sum(1 for a in apps if a.get('status') == 'completed')}
        ],
        'popular': popular,
        'recent': [a for a in apps if a.get('status') != 'cancelled'][-10:] if apps else []
    })

@app.route('/api/ai/ask', methods=['POST'])
def ask_ai():
    q = request.json.get('question', '').lower()
    data = load_data()
    apps = data['appointments']
    services = {s['name']: {'price': s['price'], 'material_cost': s.get('material_cost', 0)} for s in data['services']}
    total_revenue = 0
    total_materials = 0
    completed_count = 0
    service_counts = {}
    for a in apps:
        if a.get('status') == 'completed':
            s = services.get(a['service'])
            if s:
                total_revenue += s['price']
                total_materials += s['material_cost']
                completed_count += 1
                service_counts[a['service']] = service_counts.get(a['service'], 0) + 1
    net_profit = total_revenue - total_materials
    margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    if 'profit' in q or 'earn' in q or 'revenue' in q:
        a = f"💰 **Financial Summary:**\n\n• Total Revenue: ${total_revenue:,.2f}\n• Material Costs: ${total_materials:,.2f}\n• **Net Profit: ${net_profit:,.2f}**\n• Profit Margin: {margin:.1f}%\n• Completed Appointments: {completed_count}\n\nTo increase profit, focus on services with lower material costs like Wax (85%+ margin)!"
    elif 'predict' in q or 'forecast' in q or 'next month' in q:
        monthly_avg = total_revenue / max(1, datetime.now().month)
        projected = monthly_avg * 1.15
        a = f"📈 **Business Forecast:**\n\n• Current Monthly Average: ${monthly_avg:,.2f}\n• Next Month Projection: ${projected:,.2f}\n• Projected Net Profit: ${projected * (margin/100):,.2f}\n\nBook 15% more appointments to reach this goal! You're on track for growth 🚀"
    elif 'popular' in q or 'best' in q or 'top' in q:
        top_service = max(service_counts, key=service_counts.get) if service_counts else "No data yet"
        top_count = service_counts.get(top_service, 0)
        a = f"🎯 **Most Popular Service:**\n\n🏆 {top_service} with {top_count} bookings!\n\n💡 Tip: Promote your second-best services to balance demand and increase overall revenue. Consider bundling popular services for package deals!"
    elif 'grow' in q or 'increase' in q or 'improve' in q:
        a = f"📈 **Growth Strategies for Medical Touch:**\n\n1. ✨ **Loyalty Program** - Reward repeat customers (10th visit free!)\n2. 📱 **SMS Reminders** - Reduce no-shows by 30%\n3. 🎯 **Promote Your Bestseller** - Focus on your most popular service\n4. 💰 **Package Deals** - Bundle services for higher value\n5. ⭐ **Referral Discounts** - \"Bring a friend\" promotions\n\nImplement these to see 20-30% growth in 3 months!"
    else:
        a = f"💡 **Medical Touch Business Insights:**\n\n• 📊 Total Revenue: ${total_revenue:,.2f}\n• 💰 Net Profit: ${net_profit:,.2f}\n• 👥 Customers Served: {len(data['customers'])}\n• 📅 Appointments: {len(apps)}\n• 📈 Profit Margin: {margin:.1f}%\n\nAsk me about:\n• \"How much profit?\" - Financial summary\n• \"Predict next month\" - Business forecast\n• \"Most popular service\" - Top performers\n• \"How to grow\" - Business strategies"
    return jsonify({'answer': a})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("✨✨✨ MEDICAL TOUCH CRM - ULTIMATE EDITION ✨✨✨")
    print("="*70)
    print("\n🚀 Your CRM is now LIVE with ALL features!")
    print("\n📍 CUSTOMER WEBSITE: https://medical-touch.onrender.com")
    print("🔐 ADMIN DASHBOARD: https://medical-touch.onrender.com/admin")
    print("\n🔑 Admin Login: medicaltouch / admin123")
    print("\n✅ **ALL FEATURES INCLUDED:**")
    print("   • 60+ Services with descriptions & real prices")
    print("   • 🔍 Powerful search bar for customers")
    print("   • 💅 Nails | 👁️ Lashes | 💆 Skincare | 🕯️ Wax tabs")
    print("   • 🤖 AI Chatbot with 7 quick question buttons")
    print("   • ✅ Confirm | ⭐ Complete | ❌ Cancel | 🗑️ Delete buttons")
    print("   • 🎨 Colored appointment status cards")
    print("   • 📝 Customer notes & history")
    print("   • 💰 Most Wanted Services with revenue & profit")
    print("   • 🔔 Real-time notification bell")
    print("   • 📦 Materials & cost tracking")
    print("   • 📊 Profit wheels (Today/Week/Month/Year)")
    print("   • 🤖 Advanced AI Assistant for business insights")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
