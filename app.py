from flask import Flask, render_template_string, request, jsonify, send_from_directory, session, redirect, url_for
import json
import os
from datetime import datetime
import time
from functools import wraps

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
        'materials': {
            'Nails': {'cost': 500, 'items': ['Gel Polish', 'Acrylic Powder', 'Tips', 'Files']},
            'Lashes': {'cost': 300, 'items': ['Lash Glue', 'Lashes', 'Tweezers', 'Primer']},
            'Skincare': {'cost': 400, 'items': ['Serums', 'Masks', 'MesoNeedles', 'Products']},
            'Wax': {'cost': 200, 'items': ['Wax Beans', 'Strips', 'Oil', 'Pre/Post Care']}
        },
        'services': [
            {'id': '1', 'name': 'Full Set GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5},
            {'id': '2', 'name': 'Full Set Fiber GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5},
            {'id': '3', 'name': 'Full Set Polygel + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5},
            {'id': '4', 'name': 'Full Set Gel-X + Color Gel', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 4},
            {'id': '5', 'name': 'Full Set Acrylic', 'price': 40, 'duration': 75, 'category': 'Nails', 'material_cost': 6},
            {'id': '6', 'name': 'Dipping Powder GEL', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 4},
            {'id': '7', 'name': 'Full Set Lucid GEL', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 4},
            {'id': '8', 'name': 'Rubber Base + Color Gel', 'price': 20, 'duration': 45, 'category': 'Nails', 'material_cost': 3},
            {'id': '9', 'name': 'Gel Color + Base Gel', 'price': 15, 'duration': 30, 'category': 'Nails', 'material_cost': 2},
            {'id': '10', 'name': 'Ombre Gelish + Rubber Base', 'price': 15, 'duration': 45, 'category': 'Nails', 'material_cost': 3},
            {'id': '11', 'name': 'French Gelish + Rubber Base', 'price': 18, 'duration': 45, 'category': 'Nails', 'material_cost': 3},
            {'id': '12', 'name': 'Refill GEL', 'price': 22, 'duration': 45, 'category': 'Nails', 'material_cost': 3},
            {'id': '13', 'name': 'Remove GEL + Manicure', 'price': 15, 'duration': 30, 'category': 'Nails', 'material_cost': 2},
            {'id': '14', 'name': 'Manicure + Pose', 'price': 10, 'duration': 30, 'category': 'Nails', 'material_cost': 2},
            {'id': '15', 'name': 'Pedicure + Pose', 'price': 15, 'duration': 45, 'category': 'Nails', 'material_cost': 3},
            {'id': '16', 'name': 'Paraffin', 'price': 8, 'duration': 20, 'category': 'Nails', 'material_cost': 1},
            {'id': '17', 'name': 'Pose Verni', 'price': 5, 'duration': 15, 'category': 'Nails', 'material_cost': 1},
            {'id': '18', 'name': 'French Verni', 'price': 10, 'duration': 20, 'category': 'Nails', 'material_cost': 1},
            {'id': '19', 'name': 'Fake Nails + Color', 'price': 15, 'duration': 45, 'category': 'Nails', 'material_cost': 3},
            {'id': '20', 'name': 'Special Nail Art', 'price': 15, 'duration': 30, 'category': 'Nails', 'material_cost': 3},
            {'id': '21', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '22', 'name': 'Full Set Lashes Volume', 'price': 38, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '23', 'name': 'Full Set Lashes Mega Volume', 'price': 45, 'duration': 105, 'category': 'Lashes', 'material_cost': 6},
            {'id': '24', 'name': 'Refill Lashes', 'price': 25, 'duration': 45, 'category': 'Lashes', 'material_cost': 3},
            {'id': '25', 'name': 'Removal Lashes', 'price': 20, 'duration': 30, 'category': 'Lashes', 'material_cost': 2},
            {'id': '26', 'name': 'Facial Classic', 'price': 35, 'duration': 60, 'category': 'Skincare', 'material_cost': 4},
            {'id': '27', 'name': 'Hydra Facial', 'price': 55, 'duration': 75, 'category': 'Skincare', 'material_cost': 8},
            {'id': '28', 'name': 'Medical Facial + MesoTherapy', 'price': 65, 'duration': 90, 'category': 'Skincare', 'material_cost': 10},
            {'id': '29', 'name': 'HIFU', 'price': 100, 'duration': 90, 'category': 'Skincare', 'material_cost': 5},
            {'id': '30', 'name': 'Mesopen Whitening', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '31', 'name': 'Mesopen Acne', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '32', 'name': 'Mesopen Lifting Face', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '33', 'name': 'Mesopen Dark Circle', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '34', 'name': 'Mesopen Lip Whitening', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '35', 'name': 'Mesopen Hair Loss', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '36', 'name': 'Mesopen Hair Grow', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '37', 'name': 'Mesopen Cellulite', 'price': 35, 'duration': 45, 'category': 'Skincare', 'material_cost': 8},
            {'id': '38', 'name': 'Meso botox Injection', 'price': 100, 'duration': 60, 'category': 'Skincare', 'material_cost': 15},
            {'id': '39', 'name': 'Meso lipo double Chin', 'price': 100, 'duration': 60, 'category': 'Skincare', 'material_cost': 15},
            {'id': '40', 'name': 'Meso Fats (5 Sessions)', 'price': 200, 'duration': 60, 'category': 'Skincare', 'material_cost': 50},
            {'id': '41', 'name': 'Meso Melasma Injection', 'price': 100, 'duration': 60, 'category': 'Skincare', 'material_cost': 15},
            {'id': '42', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax', 'material_cost': 3},
            {'id': '43', 'name': 'Full Face + Neck Wax', 'price': 15, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '44', 'name': 'Full Back Wax', 'price': 18, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '45', 'name': 'Lower Back Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '46', 'name': 'Half Back Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '47', 'name': 'Full Belly Wax', 'price': 18, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '48', 'name': 'Chest Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '49', 'name': 'Full Arms Wax', 'price': 12, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '50', 'name': 'Half Arms Wax', 'price': 8, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '51', 'name': 'Under Arms Wax', 'price': 6, 'duration': 15, 'category': 'Wax', 'material_cost': 1},
            {'id': '52', 'name': 'Full Legs Wax', 'price': 17, 'duration': 45, 'category': 'Wax', 'material_cost': 1},
            {'id': '53', 'name': 'Half Legs Wax', 'price': 11, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '54', 'name': 'Full Bikini Wax', 'price': 23, 'duration': 30, 'category': 'Wax', 'material_cost': 2},
            {'id': '55', 'name': 'Bikini Line Wax', 'price': 16, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '56', 'name': 'Eyebrow Classic Wax', 'price': 4, 'duration': 10, 'category': 'Wax', 'material_cost': 0.5},
            {'id': '57', 'name': 'Eyebrow Waxing', 'price': 6, 'duration': 10, 'category': 'Wax', 'material_cost': 0.5},
            {'id': '58', 'name': 'Lips Classic Wax', 'price': 3, 'duration': 5, 'category': 'Wax', 'material_cost': 0.5},
            {'id': '59', 'name': 'Lips Wax', 'price': 5, 'duration': 10, 'category': 'Wax', 'material_cost': 0.5},
            {'id': '60', 'name': 'Nose + Chin Wax', 'price': 7, 'duration': 15, 'category': 'Wax', 'material_cost': 0.5},
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
        if a.get('staff_id') == staff_id and a.get('datetime') == datetime_str and a.get('status') != 'cancelled':
            return True
    return False

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head><title>Medical Touch Admin</title>
<style>
body{font-family:'Poppins',Arial;background:linear-gradient(135deg,#1a1a2e,#16213e);display:flex;justify-content:center;align-items:center;height:100vh;}
.login-box{background:white;padding:40px;border-radius:24px;width:380px;text-align:center;}
.login-box h2{color:#ff6b9d;margin-bottom:20px;}
input{width:100%;padding:14px;margin:10px 0;border:2px solid #eee;border-radius:12px;font-size:16px;}
button{background:#ff6b9d;color:white;border:none;padding:14px;border-radius:12px;width:100%;cursor:pointer;font-size:16px;font-weight:bold;}
.error{color:red;margin-top:15px;}
</style>
</head>
<body>
<div class="login-box">
<h2>🔐 Medical Touch Admin</h2>
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
</div>
</body>
</html>
'''CUSTOMER_HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Medical Touch | Beauty & Wellness</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Poppins',sans-serif;background:#faf8f9;}
.hero{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:60px 20px;text-align:center;position:relative;}
.hero h1{font-family:'Playfair Display',serif;font-size:52px;letter-spacing:3px;}
.hero p{font-size:16px;opacity:0.9;margin-top:10px;}
.address{background:#ff6b9d;display:inline-block;padding:10px 30px;border-radius:50px;margin-top:15px;font-size:14px;}
.tabs{display:flex;justify-content:center;gap:8px;background:white;padding:12px;box-shadow:0 4px 15px rgba(0,0,0,0.05);position:sticky;top:0;z-index:100;flex-wrap:wrap;}
.tab{padding:10px 28px;font-size:15px;font-weight:500;background:none;border:none;cursor:pointer;border-radius:40px;color:#666;transition:0.3s;}
.tab:hover{background:#ff6b9d20;color:#ff6b9d;}
.tab.active{background:#ff6b9d;color:white;box-shadow:0 4px 10px rgba(255,107,157,0.3);}
.container{max-width:1300px;margin:0 auto;padding:40px 20px;}
.tab-content{display:none;animation:fadeIn 0.4s ease;}
.tab-content.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:25px;margin-top:30px;}
.service-card{background:white;border-radius:20px;padding:22px;cursor:pointer;transition:0.3s;box-shadow:0 5px 20px rgba(0,0,0,0.03);border:1px solid #eee;}
.service-card:hover{transform:translateY(-5px);border-color:#ff6b9d;box-shadow:0 15px 30px rgba(255,107,157,0.1);}
.service-name{font-size:16px;font-weight:600;color:#1a1a2e;margin-bottom:8px;}
.service-price{font-size:26px;font-weight:bold;color:#ff6b9d;}
.service-duration{color:#aaa;font-size:12px;margin-top:8px;}
.book-hint{margin-top:12px;font-size:12px;color:#ff6b9d;font-weight:500;}
.booking-section{background:linear-gradient(135deg,#fff5f7,#ffe4e8);border-radius:28px;padding:45px;margin-top:20px;}
.booking-section h2{font-family:'Playfair Display',serif;font-size:32px;color:#1a1a2e;margin-bottom:25px;}
.form-group{margin-bottom:20px;}
input,select{width:100%;padding:14px;border:2px solid #eee;border-radius:14px;font-size:15px;font-family:'Poppins',sans-serif;transition:0.3s;}
input:focus,select:focus{outline:none;border-color:#ff6b9d;}
.submit-btn{background:#ff6b9d;color:white;border:none;padding:14px;border-radius:40px;font-size:16px;font-weight:bold;cursor:pointer;width:100%;transition:0.3s;}
.submit-btn:hover{background:#ff4d7d;transform:scale(1.02);}
.warning{color:#ff4d7d;font-size:12px;margin-top:5px;display:none;}
footer{background:#1a1a2e;color:white;text-align:center;padding:40px;margin-top:60px;}
.chat-btn{position:fixed;bottom:30px;right:30px;width:65px;height:65px;background:linear-gradient(135deg,#ff6b9d,#ff4d7d);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:30px;box-shadow:0 5px 20px rgba(0,0,0,0.2);z-index:1000;transition:0.3s;}
.chat-btn:hover{transform:scale(1.1);}
.chat-window{position:fixed;bottom:110px;right:30px;width:350px;height:480px;background:white;border-radius:20px;display:none;flex-direction:column;box-shadow:0 10px 40px rgba(0,0,0,0.2);z-index:1000;overflow:hidden;}
.chat-window.show{display:flex;}
.chat-header{background:linear-gradient(135deg,#ff6b9d,#ff4d7d);color:white;padding:15px;font-weight:bold;font-size:16px;}
.chat-messages{flex:1;overflow-y:auto;padding:15px;background:#f5f5f5;}
.bot-msg{background:white;padding:10px 15px;border-radius:18px;margin:8px 0;max-width:85%;color:#333;border:1px solid #eee;}
.user-msg{background:#ff6b9d;color:white;padding:10px 15px;border-radius:18px;margin:8px 0;max-width:85%;margin-left:auto;text-align:right;}
.chat-input{display:flex;padding:12px;border-top:1px solid #ddd;background:white;}
.chat-input input{flex:1;padding:12px;margin:0;margin-right:10px;border:1px solid #ddd;border-radius:25px;font-size:14px;}
.chat-input button{background:#ff6b9d;color:white;border:none;border-radius:25px;padding:12px 20px;cursor:pointer;font-weight:bold;}
.quick-btns{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
.quick-btn{background:#f0f0f0;border:none;padding:6px 12px;border-radius:20px;font-size:11px;cursor:pointer;}
@media(max-width:768px){.hero h1{font-size:32px;}.tab{padding:8px 18px;font-size:13px;}.services-grid{grid-template-columns:1fr;}.chat-window{width:300px;height:420px;right:10px;bottom:100px;}.chat-btn{bottom:20px;right:20px;}}
</style>
</head>
<body>
<div class="hero">
<h1>MEDICAL TOUCH</h1>
<p>Where Beauty Meets Medical Excellence</p>
<div class="address">📍 Bakaata - Ain W ZEIN Road | 📞 81023625</div>
</div>
<div class="tabs">
<button class="tab active" onclick="switchTab('nails')">💅 Nails</button>
<button class="tab" onclick="switchTab('lashes')">👁️ Lashes</button>
<button class="tab" onclick="switchTab('skincare')">💆 Skincare</button>
<button class="tab" onclick="switchTab('wax')">🕯️ Wax</button>
<button class="tab" onclick="switchTab('book')">📅 Book</button>
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
<div class="form-group"><input type="text" id="custName" placeholder="Full Name" required></div>
<div class="form-group"><input type="tel" id="custPhone" placeholder="Phone Number" required></div>
<div class="form-group"><input type="email" id="custEmail" placeholder="Email (optional)"></div>
<div class="form-group"><select id="serviceSelect" required><option value="">Select Service</option></select></div>
<div class="form-group"><input type="datetime-local" id="appointmentDate" required></div>
<div id="slotWarning" class="warning">⚠️ This time is already booked. Please choose another time.</div>
<button type="submit" class="submit-btn">Confirm Booking</button>
</form>
</div>
</div>
</div>
<footer>
<p>✨ Medical Touch - Where Beauty Meets Medical Excellence ✨</p>
<p>📍 Bakaata - Ain W ZEIN Road | 📞 81023625</p>
</footer>
<div class="chat-btn" onclick="toggleChat()">💬</div>
<div class="chat-window" id="chatWindow">
<div class="chat-header">🤖 Medical Touch AI Assistant</div>
<div class="chat-messages" id="chatMsgs">
<div class="bot-msg">Hello! 👋 I'm your beauty assistant. Ask me about nails, lashes, skincare, wax, or prices!</div>
<div class="quick-btns">
<button class="quick-btn" onclick="sendQuick('nails')">💅 Nails</button>
<button class="quick-btn" onclick="sendQuick('lashes')">👁️ Lashes</button>
<button class="quick-btn" onclick="sendQuick('skincare')">💆 Skincare</button>
<button class="quick-btn" onclick="sendQuick('wax')">🕯️ Wax</button>
<button class="quick-btn" onclick="sendQuick('price')">💰 Prices</button>
<button class="quick-btn" onclick="sendQuick('book')">📅 How to book</button>
</div>
</div>
<div class="chat-input">
<input type="text" id="chatInput" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter')sendChat()">
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
<div class="service-duration">⏱️ ${s.duration} min</div>
<div class="book-hint">Click to book →</div>
</div>`;
});
document.getElementById(elId).innerHTML = html || '<p style="text-align:center;color:#999;">Loading...</p>';
}}
function populateSelect(services){
let html = '<option value="">Select Service</option>';
services.forEach(s => { html += `<option value="${s.name.replace(/'/g, "\\'")}">${s.name} - $${s.price}</option>`; });
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
const res = await fetch('/api/customer-book', {
method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify(data)
});
const result = await res.json();
if(result.success) alert('✅ Appointment booked! We will confirm via SMS.');
else if(result.double_booking) alert('❌ Sorry, this time is already taken. Please choose another time.');
else alert('❌ Error. Please try again.');
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
if(topic==='nails') q = 'Tell me about nail services';
if(topic==='lashes') q = 'Tell me about lash services';
if(topic==='skincare') q = 'Tell me about skincare treatments';
if(topic==='wax') q = 'Tell me about wax services';
if(topic==='price') q = 'What are your prices?';
if(topic==='book') q = 'How do I book an appointment?';
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
'''ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Medical Touch | Admin Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Poppins',sans-serif;background:#f0f2f5;}
.sidebar{width:270px;background:linear-gradient(180deg,#1a1a2e,#16213e);color:white;position:fixed;height:100%;padding:30px 20px;overflow-y:auto;}
.sidebar h2{font-size:22px;margin-bottom:40px;text-align:center;}
.sidebar nav a{display:block;color:white;text-decoration:none;padding:12px 18px;margin:8px 0;border-radius:12px;transition:0.3s;cursor:pointer;}
.sidebar nav a:hover{background:#ff6b9d;transform:translateX(5px);}
.main{margin-left:270px;padding:25px;}
.top-bar{background:white;padding:18px 25px;border-radius:18px;margin-bottom:25px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px rgba(0,0,0,0.05);}
.top-bar h2{color:#1a1a2e;}
.logout-btn{background:#ff4d7d;color:white;border:none;padding:10px 25px;border-radius:30px;cursor:pointer;font-weight:500;}
.wheels-container{display:grid;grid-template-columns:1fr 1fr;gap:25px;margin-bottom:30px;}
.wheel-card{background:white;border-radius:20px;padding:25px;text-align:center;box-shadow:0 5px 20px rgba(0,0,0,0.05);}
.wheel-card h3{color:#1a1a2e;margin-bottom:20px;font-size:18px;}
.wheel{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;}
.wheel-item{width:105px;height:105px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;cursor:pointer;transition:0.3s;}
.wheel-item:hover{transform:scale(1.05);}
.wheel-item span{font-size:22px;font-weight:bold;}
.wheel-item div{font-size:12px;margin-top:5px;}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px;}
.stat-card{background:white;border-radius:18px;padding:22px;text-align:center;box-shadow:0 5px 20px rgba(0,0,0,0.05);}
.stat-card .number{font-size:36px;font-weight:bold;color:#ff6b9d;}
.stat-card p{color:#666;font-size:14px;margin-top:8px;}
.section{background:white;border-radius:20px;padding:25px;margin-bottom:25px;display:none;box-shadow:0 5px 20px rgba(0,0,0,0.05);}
.section.active{display:block;}
.section h2{color:#1a1a2e;margin-bottom:20px;font-size:22px;}
table{width:100%;border-collapse:collapse;}
th,td{padding:12px;text-align:left;border-bottom:1px solid #eee;}
th{background:#fef8f9;color:#ff6b9d;font-weight:600;}
.delete-btn{background:#dc3545;color:white;border:none;padding:5px 12px;border-radius:6px;cursor:pointer;}
.edit-btn{background:#ffc107;color:#333;border:none;padding:5px 12px;border-radius:6px;cursor:pointer;}
input,select{padding:10px;margin:5px;border:1px solid #ddd;border-radius:8px;}
button{background:#ff6b9d;color:white;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;font-weight:500;}
.profit-detail{margin-top:15px;padding:15px;background:#fef8f9;border-radius:12px;display:none;font-size:14px;}
.ai-box{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:20px;padding:30px;color:white;}
.ai-box input{width:70%;padding:12px;border:none;border-radius:30px;}
.ai-box button{background:white;color:#764ba2;border:none;padding:12px 25px;border-radius:30px;cursor:pointer;font-weight:bold;margin-left:10px;}
.ai-response{margin-top:20px;padding:15px;background:rgba(255,255,255,0.2);border-radius:12px;display:none;}
.floating-bell{position:fixed;bottom:30px;right:30px;width:65px;height:65px;background:linear-gradient(135deg,#ff6b9d,#ff4d7d);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:30px;box-shadow:0 5px 20px rgba(0,0,0,0.2);z-index:1000;}
.bell-badge{position:absolute;top:-5px;right:-5px;background:#dc3545;color:white;border-radius:50%;width:22px;height:22px;font-size:12px;display:flex;align-items:center;justify-content:center;}
.notif-popup{position:fixed;bottom:110px;right:30px;width:320px;background:white;border-radius:15px;display:none;box-shadow:0 10px 30px rgba(0,0,0,0.2);z-index:1000;}
.notif-popup.show{display:block;}
.notif-header{background:#ff6b9d;color:white;padding:12px;border-radius:15px 15px 0 0;font-weight:bold;}
.notif-list{max-height:350px;overflow-y:auto;}
.notif-item{padding:12px;border-bottom:1px solid #eee;font-size:13px;}
.notif-time{font-size:10px;color:#999;margin-top:5px;}
@media(max-width:768px){.sidebar{width:100%;height:auto;position:relative;}.main{margin-left:0;}.wheels-container{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="sidebar">
<h2>💅 MEDICAL TOUCH</h2>
<nav>
<a onclick="showSection('dashboard')">📊 Dashboard</a>
<a onclick="showSection('materials')">📦 Materials & Costs</a>
<a onclick="showSection('customers')">👥 Customers</a>
<a onclick="showSection('appointments')">📅 Appointments</a>
<a onclick="showSection('services')">💅 Services</a>
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
<h3>💰 Profit Wheels</h3>
<div class="wheel">
<div class="wheel-item" style="background:#1a1a2e;" onclick="showProfit('today')"><span id="todayAmt">$0</span><div>Today</div></div>
<div class="wheel-item" style="background:#ff6b9d;" onclick="showProfit('week')"><span id="weekAmt">$0</span><div>Week</div></div>
<div class="wheel-item" style="background:#ff4d7d;" onclick="showProfit('month')"><span id="monthAmt">$0</span><div>Month</div></div>
<div class="wheel-item" style="background:#1a1a2e;" onclick="showProfit('year')"><span id="yearAmt">$0</span><div>Year</div></div>
</div>
<div id="profitDetail" class="profit-detail"></div>
</div>
<div class="wheel-card">
<h3>🎯 Most Wanted Services</h3>
<div id="popularWheel" class="wheel"></div>
<div id="popularDetail" class="profit-detail"></div>
</div>
</div>
<div class="stats-grid" id="statsGrid"></div>
<h3 style="margin:20px 0 15px 0;">📋 Recent Bookings</h3>
<div id="recentList"></div>
</div>
<div id="materials" class="section">
<h2>📦 Materials & Monthly Costs</h2>
<div id="materialsGrid"></div>
<div id="profitSummary" style="margin-top:20px;padding:20px;background:#fef8f9;border-radius:15px;"></div>
</div>
<div id="customers" class="section">
<h2>👥 Customer Directory</h2>
<div id="customerTable"></div>
</div>
<div id="appointments" class="section">
<h2>📅 Appointment Manager</h2>
<div id="appointmentTable"></div>
</div>
<div id="services" class="section">
<h2>💅 Service Manager</h2>
<div style="margin-bottom:20px;display:flex;flex-wrap:wrap;gap:10px;">
<input type="text" id="newName" placeholder="Service Name" style="width:200px;">
<input type="number" id="newPrice" placeholder="Price $" style="width:100px;">
<select id="newCat" style="width:120px;">
<option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option>
</select>
<input type="number" id="newCost" placeholder="Material Cost $" style="width:130px;">
<button onclick="addService()">➕ Add Service</button>
</div>
<div id="serviceTable"></div>
</div>
<div id="ai" class="section">
<div class="ai-box">
<h2>🤖 AI Business Assistant</h2>
<p>Ask me anything about profits, popular services, or predictions!</p>
<div style="margin-top:20px;">
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
if(s==='materials') loadMaterials();
if(s==='customers') loadCustomers();
if(s==='appointments') loadAppointments();
if(s==='services') loadServices();
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
popularHtml += `<div class="wheel-item" style="background:${colors[i%colors.length]}" onclick="showPopular('${p.name.replace(/'/g, "\\'")}')"><span>${p.name.substring(0,8)}</span><div>${p.count}</div></div>`;
});
document.getElementById('popularWheel').innerHTML = popularHtml || '<p>No data yet</p>';
let recentHtml = '';
d.recent.forEach(a => {
recentHtml += `<div style="padding:12px;margin:8px 0;border-left:4px solid #ff6b9d;background:#f8f9fa;border-radius:8px;"><strong>${a.customer_name}</strong> - ${a.service}<br>📅 ${a.datetime} | Status: ${a.status}</div>`;
});
document.getElementById('recentList').innerHTML = recentHtml || '<p>No appointments yet</p>';
}
function showProfit(p){
const d = document.getElementById('profitDetail');
let msg = '';
if(p==='today') msg = '💰 Today: $'+profitData.today+' ('+(profitData.todayCount||0)+' appts) | Net: $'+(profitData.todayNet||0);
if(p==='week') msg = '💰 Week: $'+profitData.week+' ('+(profitData.weekCount||0)+' appts) | Net: $'+(profitData.weekNet||0);
if(p==='month') msg = '💰 Month: $'+profitData.month+' ('+(profitData.monthCount||0)+' appts) | Net: $'+(profitData.monthNet||0);
if(p==='year') msg = '💰 Year: $'+profitData.year+' ('+(profitData.yearCount||0)+' appts) | Net: $'+(profitData.yearNet||0);
d.innerHTML = msg;
d.style.display = 'block';
setTimeout(()=>d.style.display='none',4000);
}
function showPopular(n){
const d = document.getElementById('popularDetail');
const p = popularData.find(x => x.name === n);
if(p) d.innerHTML = '🎯 '+p.name+': '+p.count+' bookings | Net: $'+(p.netProfit||0);
d.style.display = 'block';
setTimeout(()=>d.style.display='none',4000);
}
async function loadMaterials(){
const r = await fetch('/api/materials');
const d = await r.json();
let html = '<table><tr><th>Category</th><th>Monthly Cost</th><th>Items</th><th>Action</th></tr>';
for(let cat in d.materials){
html += `<tr><td><strong>${cat}</strong></td><td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:80px"> $</td><td>${d.materials[cat].items.join(', ')}</td><td><button onclick="updateCost('${cat}')">Update</button></td></tr>`;
}
html += '</table>';
document.getElementById('materialsGrid').innerHTML = html;
document.getElementById('profitSummary').innerHTML = `<h3>💰 Financial Summary</h3><p>Total Revenue: $${d.totalRevenue} | Materials: $${d.totalMaterialCost} | <strong>Net Profit: $${d.netProfit}</strong></p><p>Margin: ${((d.netProfit/d.totalRevenue)*100).toFixed(1)}%</p>`;
}
async function updateCost(cat){
const cost = document.getElementById('cost_'+cat).value;
await fetch('/api/materials/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat,cost:parseInt(cost)})});
loadMaterials();
}
async function loadCustomers(){
const r = await fetch('/api/customers');
const c = await r.json();
let h = '<table><tr><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Action</th></tr>';
c.forEach(cust => { h += `<tr><td>${cust.name}</td><td>${cust.phone}</td><td>${cust.email||'-'}</td><td>${cust.visits||0}</td><td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button></td></tr>`; });
h += '</table>';
document.getElementById('customerTable').innerHTML = h;
}
async function loadAppointments(){
const r = await fetch('/api/appointments');
const a = await r.json();
let h = '<table><tr><th>Customer</th><th>Service</th><th>Time</th><th>Status</th><th>Action</th></tr>';
a.forEach(app => {
h += `<tr><td>${app.customer_name}</td><td>${app.service}</td><td>${app.datetime}</td><td><select onchange="updateStatus('${app.id}',this.value)"><option ${app.status==='pending'?'selected':''}>pending</option><option ${app.status==='confirmed'?'selected':''}>confirmed</option><option ${app.status==='completed'?'selected':''}>completed</option></select></td><td><button class="delete-btn" onclick="deleteAppointment('${app.id}')">Cancel</button></td></tr>`;
});
h += '</table>';
document.getElementById('appointmentTable').innerHTML = h;
}
async function loadServices(){
const r = await fetch('/api/services');
const s = await r.json();
let h = '<table><tr><th>Service</th><th>Price</th><th>Duration</th><th>Category</th><th>Material</th><th>Action</th></tr>';
s.forEach(serv => { h += `<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.duration}min</td><td>${serv.category}</td><td>$${serv.material_cost||0}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td></tr>`; });
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
}
async function deleteService(id){ if(confirm('Delete?')){ await fetch('/api/services/'+id,{method:'DELETE'}); loadServices(); } }
async function deleteCustomer(id){ if(confirm('Delete?')){ await fetch('/api/customers/'+id,{method:'DELETE'}); loadCustomers(); loadDashboard(); } }
async function deleteAppointment(id){ if(confirm('Cancel?')){ await fetch('/api/appointments/'+id,{method:'DELETE'}); loadAppointments(); loadDashboard(); } }
async function updateStatus(id,status){ await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:status})}); loadDashboard(); loadAppointments(); }
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
document.getElementById('notifList').innerHTML = h || '<div class="notif-item">No notifications</div>';
if(n.length>lastCount && lastCount>0){ document.querySelector('.floating-bell').style.transform='scale(1.2)'; setTimeout(()=>document.querySelector('.floating-bell').style.transform='scale(1)',300); }
lastCount = n.length;
}
function toggleNotif(){ const p = document.getElementById('notifPopup'); p.classList.toggle('show'); if(p.classList.contains('show')) loadNotif(); }
loadDashboard(); loadNotif(); setInterval(()=>{ if(document.getElementById('dashboard').classList.contains('active')) loadDashboard(); loadNotif(); },15000);
</script>
</body>
</html>
'''# API ROUTES
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
    if 'nail' in q or 'manicure' in q:
        a = "💅 We offer Gel, Acrylic, Polygel, Dip Powder. Full sets $30-40, Manicure $10. Book now!"
    elif 'lash' in q or 'lashes' in q:
        a = "👁️ Classic $35, Volume $38, Mega Volume $45. Refills $25. Lasts 3-4 weeks!"
    elif 'skin' in q or 'facial' in q or 'meso' in q or 'derma' in q:
        a = "💆 Facials $35-65, HydraFacial $55, Mesotherapy $35-100, HIFU $100. Results guaranteed!"
    elif 'wax' in q:
        a = "🕯️ Full body $45, Full legs $17, Bikini $23. Pain-free experience!"
    elif 'price' in q or 'cost' in q:
        a = "💰 Nails: $10-40, Lashes: $35-45, Skincare: $35-200, Wax: $3-45. Best value in town!"
    elif 'book' in q or 'appointment' in q:
        a = "📅 Go to Book tab, select service, pick date/time. We'll confirm by SMS! Or call 81023625."
    elif 'location' in q or 'address' in q or 'where' in q:
        a = "📍 Bakaata - Ain W ZEIN Road. Open daily 10AM-8PM. Call 81023625 for directions!"
    else:
        a = "✨ Medical Touch: Nails, Lashes, Skincare, Waxing. Ask about any service, prices, or booking!"
    return jsonify({'answer': a})

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(load_data()['services'])

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
        cust = {'id': str(len(data['customers']) + 1), 'name': b['name'], 'phone': b['phone'], 'email': b.get('email', ''), 'visits': 0}
        data['customers'].append(cust)
    appt = {'id': str(len(data['appointments']) + 1), 'customer_id': cust['id'], 'customer_name': cust['name'], 'service': b['service'], 'datetime': b['datetime'], 'status': 'pending', 'staff_id': 'staff1', 'booked_at': datetime.now().isoformat()}
    data['appointments'].append(appt)
    save_data(data)
    add_notification(f"📅 NEW: {cust['name']} booked {b['service']} at {b['datetime']}")
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

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    return jsonify(load_data()['appointments'])

@app.route('/api/appointments/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    data = load_data()
    data['appointments'] = [a for a in data['appointments'] if a['id'] != appointment_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/appointments/<appointment_id>/status', methods=['PUT'])
def update_status(appointment_id):
    data = load_data()
    status = request.json.get('status')
    for a in data['appointments']:
        if a['id'] == appointment_id:
            a['status'] = status
            if status == 'completed':
                cust = next((c for c in data['customers'] if c['id'] == a['customer_id']), None)
                if cust:
                    cust['visits'] = cust.get('visits', 0) + 1
                add_notification(f"✅ Completed: {a['customer_name']} - {a['service']}")
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

@app.route('/api/notifications/clear', methods=['DELETE'])
def clear_notifications():
    save_notifications([])
    return jsonify({'success': True})

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
    for a in apps:
        if a.get('status') == 'completed':
            s = services.get(a['service'])
            if s:
                pop[a['service']] = pop.get(a['service'], 0) + 1
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
                except: pass
    popular = [{'name': n, 'count': c, 'netProfit': 0} for n, c in sorted(pop.items(), key=lambda x: x[1], reverse=True)[:6]]
    return jsonify({
        'profit': {
            'today': t_rev, 'week': w_rev, 'month': m_rev, 'year': y_rev,
            'todayNet': t_rev - t_mat, 'weekNet': w_rev - w_mat,
            'monthNet': m_rev - m_mat, 'yearNet': y_rev - y_mat,
            'todayCount': t_cnt, 'weekCount': w_cnt, 'monthCount': m_cnt, 'yearCount': y_cnt
        },
        'stats': [
            {'title': '👥 Customers', 'value': len(data['customers'])},
            {'title': '📅 Appointments', 'value': len(apps)},
            {'title': '⏳ Pending', 'value': sum(1 for a in apps if a.get('status') == 'pending')},
            {'title': '✅ Completed', 'value': sum(1 for a in apps if a.get('status') == 'completed')}
        ],
        'popular': popular,
        'recent': apps[-10:] if apps else []
    })

@app.route('/api/ai/ask', methods=['POST'])
def ask_ai():
    q = request.json.get('question', '').lower()
    data = load_data()
    apps = data['appointments']
    services = {s['name']: {'price': s['price'], 'material_cost': s.get('material_cost', 0)} for s in data['services']}
    total = 0
    materials = 0
    for a in apps:
        if a.get('status') == 'completed':
            s = services.get(a['service'])
            if s:
                total += s['price']
                materials += s['material_cost']
    net = total - materials
    if 'profit' in q:
        a = f"💰 Revenue: ${total}, Materials: ${materials}, Net: ${net}. Margin: {((net/total)*100) if total>0 else 0:.1f}%"
    elif 'predict' in q or 'forecast' in q:
        a = f"📈 Next month projection: ${(total/12)*1.15:.2f} if you maintain current pace. Book 15% more to exceed!"
    elif 'popular' in q or 'best' in q:
        from collections import Counter
        service_counts = Counter([a['service'] for a in apps if a.get('status') == 'completed'])
        top = service_counts.most_common(1)[0][0] if service_counts else 'No data'
        a = f"🎯 Your most popular service is {top}! Promote your second-best to balance demand."
    else:
        a = f"💡 You have {len(data['customers'])} customers, {len(apps)} appointments, ${net} net profit. Ask about profits, predictions, or popular services!"
    return jsonify({'answer': a})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✨ MEDICAL TOUCH CRM v3.0 - COMPLETE! ✨")
    print("="*60)
    print("\n📍 CUSTOMER: https://medical-touch.onrender.com")
    print("🔐 ADMIN: https://medical-touch.onrender.com/admin")
    print("\n🔑 Admin Login: medicaltouch / admin123")
    print("\n✅ ALL FEATURES:")
    print("   • 60+ Services with real prices")
    print("   • Tabs for Nails, Lashes, Skincare, Wax")
    print("   • Floating AI Chatbot for customers")
    print("   • Admin Dashboard with Materials")
    print("   • Floating Notification Bell")
    print("   • Profit Wheels (Today/Week/Month/Year)")
    print("   • Most Wanted Services Wheel")
    print("   • Double-booking prevention")
    print("   • Real-time notifications")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
