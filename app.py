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
        'materials': {
            'Nails': {'cost': 500, 'items': ['Gel Polish', 'Acrylic Powder', 'Tips', 'Files']},
            'Lashes': {'cost': 300, 'items': ['Lash Glue', 'Lashes', 'Tweezers', 'Primer']},
            'Skincare': {'cost': 400, 'items': ['Serums', 'Masks', 'MesoNeedles']},
            'Wax': {'cost': 200, 'items': ['Wax Beans', 'Strips', 'Oil']}
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
        if a.get('staff_id') == staff_id and a.get('datetime') == datetime_str and a.get('status') not in ['cancelled', 'completed']:
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
.hero{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:60px 20px;text-align:center;}
.hero h1{font-family:'Playfair Display',serif;font-size:52px;}
.address{background:#ff6b9d;display:inline-block;padding:10px 30px;border-radius:50px;margin-top:15px;}
.search-bar{max-width:500px;margin:20px auto 0;}
.search-bar input{width:100%;padding:14px 20px;border:2px solid #ff6b9d;border-radius:50px;font-size:16px;}
.tabs{display:flex;justify-content:center;gap:8px;background:white;padding:12px;position:sticky;top:0;}
.tab{padding:10px 28px;font-size:15px;background:none;border:none;cursor:pointer;border-radius:40px;color:#666;}
.tab.active{background:#ff6b9d;color:white;}
.container{max-width:1300px;margin:0 auto;padding:40px 20px;}
.tab-content{display:none;}
.tab-content.active{display:block;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:25px;margin-top:30px;}
.service-card{background:white;border-radius:20px;padding:22px;cursor:pointer;border:1px solid #eee;}
.service-card:hover{transform:translateY(-3px);border-color:#ff6b9d;}
.service-name{font-weight:600;}
.service-price{font-size:24px;font-weight:bold;color:#ff6b9d;}
.booking-section{background:#ffe4e8;border-radius:28px;padding:40px;margin-top:20px;}
input,select{width:100%;padding:14px;border:2px solid #eee;border-radius:14px;margin:10px 0;}
.submit-btn{background:#ff6b9d;color:white;border:none;padding:14px;border-radius:40px;width:100%;cursor:pointer;}
footer{background:#1a1a2e;color:white;text-align:center;padding:40px;margin-top:60px;}
.chat-btn{position:fixed;bottom:30px;right:30px;width:60px;height:60px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;}
.chat-window{position:fixed;bottom:110px;right:30px;width:350px;height:450px;background:white;border-radius:20px;display:none;flex-direction:column;box-shadow:0 10px 30px rgba(0,0,0,0.2);}
.chat-window.show{display:flex;}
.chat-header{background:#ff6b9d;color:white;padding:12px;border-radius:20px 20px 0 0;}
.chat-messages{flex:1;overflow-y:auto;padding:15px;background:#f5f5f5;}
.bot-msg{background:white;padding:8px 12px;border-radius:15px;margin:5px 0;}
.user-msg{background:#ff6b9d;color:white;padding:8px 12px;border-radius:15px;margin:5px 0;text-align:right;}
.chat-input{display:flex;padding:12px;border-top:1px solid #ddd;}
.chat-input input{flex:1;padding:10px;margin:0;margin-right:10px;border:1px solid #ddd;border-radius:25px;}
.chat-input button{background:#ff6b9d;color:white;border:none;border-radius:25px;padding:10px 15px;cursor:pointer;}
@media(max-width:768px){.hero h1{font-size:32px;}.tab{padding:8px 18px;}}
</style>
</head>
<body>
<div class="hero">
<h1>MEDICAL TOUCH</h1>
<p>Where Beauty Meets Medical Excellence</p>
<div class="address">📍 Bakaata - Ain W ZEIN Road | 📞 81023625</div>
<div class="search-bar"><input type="text" id="searchInput" placeholder="🔍 Search services..." onkeyup="searchServices()"></div>
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
<input type="text" id="custName" placeholder="Full Name" required>
<input type="tel" id="custPhone" placeholder="Phone Number" required>
<input type="email" id="custEmail" placeholder="Email">
<select id="serviceSelect" required><option value="">Select Service</option></select>
<input type="datetime-local" id="appointmentDate" required>
<div id="slotWarning" style="color:red;font-size:12px;display:none;">⚠️ Time already booked</div>
<button type="submit" class="submit-btn">Confirm Booking</button>
</form>
</div>
</div>
</div>
<footer><p>Medical Touch - Bakaata - Ain W ZEIN Road | 81023625</p></footer>
<div class="chat-btn" onclick="toggleChat()">💬</div>
<div class="chat-window" id="chatWindow">
<div class="chat-header">🤖 AI Assistant</div>
<div class="chat-messages" id="chatMsgs">
<div class="bot-msg">Hello! Ask me about nails, lashes, skincare, or wax!</div>
</div>
<div class="chat-input">
<input type="text" id="chatInput" placeholder="Ask me..." onkeypress="if(event.key==='Enter')sendChat()">
<button onclick="sendChat()">Send</button>
</div>
</div>
<script>
let services = [];
fetch('/api/services').then(r=>r.json()).then(s=>{services=s;displayServices(s);populateSelect(s);});
function displayServices(s){const cats={Nails:'nailsGrid',Lashes:'lashesGrid',Skincare:'skincareGrid',Wax:'waxGrid'};for(let[cat,id]of Object.entries(cats)){let f=s.filter(x=>x.category===cat);let html='';f.forEach(ss=>{html+=`<div class="service-card" onclick="bookService('${ss.name}')"><div class="service-name">${ss.name}</div><div class="service-price">$${ss.price}</div><div>${ss.duration} min</div><div style="color:#ff6b9d;margin-top:10px;">Click to book →</div></div>`;});document.getElementById(id).innerHTML=html||'<p>Loading...</p>';}}
function searchServices(){const term=document.getElementById('searchInput').value.toLowerCase();const cats=['nails','lashes','skincare','wax'];for(let cat of cats){const grid=document.getElementById(cat+'Grid');const cards=grid.querySelectorAll('.service-card');cards.forEach(card=>{const name=card.querySelector('.service-name').innerText.toLowerCase();card.style.display=(term===''||name.includes(term))?'block':'none';});}}
function populateSelect(s){let html='<option value="">Select Service</option>';s.forEach(ss=>{html+=`<option value="${ss.name}">${ss.name} - $${ss.price}</option>`;});document.getElementById('serviceSelect').innerHTML=html;}
function bookService(name){document.getElementById('serviceSelect').value=name;switchTab('book');}
function switchTab(tab){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));document.getElementById(tab).classList.add('active');}
document.getElementById('appointmentDate').onchange=async function(){const r=await fetch('/api/check-slot',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({datetime:this.value})});const d=await r.json();document.getElementById('slotWarning').style.display=d.booked?'block':'none';};
document.getElementById('bookingForm').onsubmit=async(e)=>{e.preventDefault();const data={name:document.getElementById('custName').value,phone:document.getElementById('custPhone').value,email:document.getElementById('custEmail').value,service:document.getElementById('serviceSelect').value,datetime:document.getElementById('appointmentDate').value};const r=await fetch('/api/customer-book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const res=await r.json();if(res.success)alert('✅ Booked!');else if(res.double_booking)alert('❌ Time taken');else alert('❌ Error');if(res.success)document.getElementById('bookingForm').reset();};
function toggleChat(){document.getElementById('chatWindow').classList.toggle('show');}
async function sendChat(){const q=document.getElementById('chatInput').value;if(!q)return;const msgs=document.getElementById('chatMsgs');msgs.innerHTML+=`<div class="user-msg">${q}</div>`;document.getElementById('chatInput').value='';const r=await fetch('/api/ai/customer-chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();msgs.innerHTML+=`<div class="bot-msg">${d.answer}</div>`;msgs.scrollTop=msgs.scrollHeight;}
</script>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Medical Touch Admin</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:Arial;background:#f0f2f5;}
.sidebar{width:250px;background:#1a1a2e;color:white;position:fixed;height:100%;padding:20px;}
.sidebar h2{text-align:center;margin-bottom:30px;}
.sidebar nav a{display:block;color:white;padding:10px;margin:5px 0;border-radius:8px;cursor:pointer;}
.sidebar nav a:hover{background:#ff6b9d;}
.main{margin-left:250px;padding:20px;}
.top-bar{background:white;padding:15px;border-radius:10px;margin-bottom:20px;display:flex;justify-content:space-between;}
.logout-btn{background:#ff4d7d;color:white;border:none;padding:8px 15px;border-radius:20px;cursor:pointer;}
.wheels-container{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;}
.wheel-card{background:white;border-radius:15px;padding:20px;text-align:center;}
.wheel{display:flex;justify-content:center;gap:15px;flex-wrap:wrap;}
.wheel-item{width:90px;height:90px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;cursor:pointer;}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:20px;}
.stat-card{background:white;border-radius:12px;padding:15px;text-align:center;}
.stat-card .number{font-size:28px;font-weight:bold;color:#ff6b9d;}
.section{background:white;border-radius:15px;padding:20px;margin-bottom:20px;display:none;}
.section.active{display:block;}
table{width:100%;border-collapse:collapse;}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;}
.delete-btn{background:#dc3545;color:white;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;}
input,select{padding:8px;margin:5px;border:1px solid #ddd;border-radius:5px;}
button{background:#ff6b9d;color:white;border:none;padding:8px 12px;border-radius:5px;cursor:pointer;}
.profit-detail{margin-top:10px;padding:10px;background:#fef8f9;border-radius:8px;display:none;}
.appointment-tabs{display:flex;gap:10px;margin-bottom:15px;}
.appt-tab{padding:8px 15px;cursor:pointer;border:none;background:#eee;border-radius:20px;}
.appt-tab.active{background:#ff6b9d;color:white;}
.appointment-list{display:none;}
.appointment-list.active{display:block;}
.appt-card{padding:12px;margin:8px 0;border-radius:8px;display:flex;justify-content:space-between;align-items:center;}
.status-pending{background:#fff5f5;border-left:3px solid #dc3545;}
.status-confirmed{background:#f0fff4;border-left:3px solid #28a745;}
.status-completed{background:#e8f4fd;border-left:3px solid #007bff;}
.status-cancelled{background:#f8f9fa;border-left:3px solid #6c757d;}
.btn-confirm{background:#28a745;color:white;border:none;padding:4px 8px;border-radius:5px;cursor:pointer;}
.btn-complete{background:#007bff;color:white;border:none;padding:4px 8px;border-radius:5px;cursor:pointer;}
.btn-cancel{background:#ffc107;color:#333;border:none;padding:4px 8px;border-radius:5px;cursor:pointer;}
.btn-delete{background:#dc3545;color:white;border:none;padding:4px 8px;border-radius:5px;cursor:pointer;}
.notes-input{width:100%;padding:6px;margin-top:5px;border:1px solid #ddd;border-radius:5px;}
.floating-bell{position:fixed;bottom:20px;right:20px;width:50px;height:50px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:25px;}
.bell-badge{position:absolute;top:-5px;right:-5px;background:#dc3545;border-radius:50%;width:18px;height:18px;font-size:10px;display:flex;align-items:center;justify-content:center;}
.notif-popup{position:fixed;bottom:80px;right:20px;width:280px;background:white;border-radius:10px;display:none;box-shadow:0 5px 15px rgba(0,0,0,0.2);}
.notif-popup.show{display:block;}
.notif-header{background:#ff6b9d;color:white;padding:8px;border-radius:10px 10px 0 0;}
.notif-item{padding:8px;border-bottom:1px solid #eee;font-size:12px;}
.ai-box{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:15px;padding:20px;color:white;}
.ai-box input{width:60%;padding:8px;border-radius:20px;border:none;}
</style>
</head>
<body>
<div class="sidebar"><h2>💅 MEDICAL TOUCH</h2><nav><a onclick="showSection('dashboard')">📊 Dashboard</a><a onclick="showSection('customers')">👥 Customers</a><a onclick="showSection('appointments')">📅 Appointments</a><a onclick="showSection('services')">💅 Services</a><a onclick="showSection('materials')">📦 Materials</a><a onclick="showSection('ai')">🤖 AI</a></nav></div>
<div class="main"><div class="top-bar"><h2>Admin Dashboard</h2><button class="logout-btn" onclick="location.href='/admin/logout'">Logout</button></div>
<div id="dashboard" class="section active"><div class="wheels-container"><div class="wheel-card"><h3>💰 Profit</h3><div class="wheel"><div class="wheel-item" style="background:#1a1a2e" onclick="showProfit('today')"><span id="todayAmt">$0</span><div>Today</div></div><div class="wheel-item" style="background:#ff6b9d" onclick="showProfit('week')"><span id="weekAmt">$0</span><div>Week</div></div><div class="wheel-item" style="background:#ff4d7d" onclick="showProfit('month')"><span id="monthAmt">$0</span><div>Month</div></div><div class="wheel-item" style="background:#1a1a2e" onclick="showProfit('year')"><span id="yearAmt">$0</span><div>Year</div></div></div><div id="profitDetail" class="profit-detail"></div></div><div class="wheel-card"><h3>🎯 Most Wanted</h3><div id="popularWheel" class="wheel"></div><div id="popularDetail" class="profit-detail"></div></div></div><div class="stats-grid" id="statsGrid"></div><h3>Recent Bookings</h3><div id="recentList"></div></div>
<div id="customers" class="section"><h2>Customers</h2><div id="customerTable"></div></div>
<div id="appointments" class="section"><h2>Appointments</h2><div class="appointment-tabs"><button class="appt-tab active" onclick="filterApps('pending')">⏳ Pending</button><button class="appt-tab" onclick="filterApps('confirmed')">✅ Confirmed</button><button class="appt-tab" onclick="filterApps('completed')">⭐ Completed</button><button class="appt-tab" onclick="filterApps('cancelled')">❌ Cancelled</button></div><div id="pendingList" class="appointment-list active"></div><div id="confirmedList" class="appointment-list"></div><div id="completedList" class="appointment-list"></div><div id="cancelledList" class="appointment-list"></div></div>
<div id="services" class="section"><h2>Services</h2><div><input type="text" id="newName" placeholder="Name"><input type="number" id="newPrice" placeholder="Price"><select id="newCat"><option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option></select><input type="number" id="newCost" placeholder="Material Cost"><button onclick="addService()">Add</button></div><div id="serviceTable"></div></div>
<div id="materials" class="section"><h2>Materials</h2><div id="materialsGrid"></div><div id="profitSummary"></div></div>
<div id="ai" class="section"><div class="ai-box"><h2>🤖 AI Assistant</h2><p>Ask about profits or predictions</p><input type="text" id="aiQuestion" placeholder="How much profit?"><button onclick="askAI()">Ask</button><div id="aiResponse"></div></div></div></div>
<div class="floating-bell" onclick="toggleNotif()">🔔<span id="bellBadge" class="bell-badge" style="display:none;">0</span></div>
<div id="notifPopup" class="notif-popup"><div class="notif-header">Notifications</div><div id="notifList"></div></div>
<script>
let profitData={},popularData=[];
function showSection(s){document.querySelectorAll('.section').forEach(sec=>sec.classList.remove('active'));document.getElementById(s).classList.add('active');if(s==='dashboard')loadDashboard();if(s==='customers')loadCustomers();if(s==='appointments')loadAppointments();if(s==='services')loadServices();if(s==='materials')loadMaterials();}
async function loadDashboard(){const r=await fetch('/api/admin/stats');const d=await r.json();profitData=d.profit;popularData=d.popular;document.getElementById('todayAmt').innerText='$'+profitData.today;document.getElementById('weekAmt').innerText='$'+profitData.week;document.getElementById('monthAmt').innerText='$'+profitData.month;document.getElementById('yearAmt').innerText='$'+profitData.year;let s='';d.stats.forEach(st=>{s+=`<div class="stat-card"><div class="number">${st.value}</div><p>${st.title}</p></div>`;});document.getElementById('statsGrid').innerHTML=s;let ph='';const cols=['#ff6b9d','#ff4d7d','#ffb347','#4ecdc4'];popularData.forEach((p,i)=>{ph+=`<div class="wheel-item" style="background:${cols[i%cols.length]}" onclick="showPopular('${p.name}')"><span>${p.name.substring(0,6)}</span><div>${p.count}</div><div style="font-size:10px">$${p.revenue}</div></div>`;});document.getElementById('popularWheel').innerHTML=ph||'<p>No data</p>';let rh='';d.recent.forEach(a=>{rh+=`<div class="status-${a.status} appt-card"><div><strong>${a.customer_name}</strong> - ${a.service}<br>📅 ${a.datetime}</div></div>`;});document.getElementById('recentList').innerHTML=rh||'<p>No appointments</p>';}
function showProfit(p){const d=document.getElementById('profitDetail');let msg='';if(p==='today')msg=`💰 Today: $${profitData.today} | Net: $${profitData.todayNet||0}`;if(p==='week')msg=`💰 Week: $${profitData.week} | Net: $${profitData.weekNet||0}`;if(p==='month')msg=`💰 Month: $${profitData.month} | Net: $${profitData.monthNet||0}`;if(p==='year')msg=`💰 Year: $${profitData.year} | Net: $${profitData.yearNet||0}`;d.innerHTML=msg;d.style.display='block';setTimeout(()=>d.style.display='none',3000);}
function showPopular(n){const d=document.getElementById('popularDetail');const p=popularData.find(x=>x.name===n);if(p)d.innerHTML=`🎯 ${p.name}: ${p.count} bookings | Revenue: $${p.revenue} | Net: $${p.netProfit}`;d.style.display='block';setTimeout(()=>d.style.display='none',3000);}
async function loadCustomers(){const r=await fetch('/api/customers');const c=await r.json();let h='<table><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Notes</th><th>Action</th></tr>';c.forEach(cust=>{h+=`<tr><td>${cust.name}</td><td>${cust.phone}</td><td>${cust.email||'-'}</td><td>${cust.visits||0}</td><td><input type="text" id="note_${cust.id}" value="${cust.notes||''}" placeholder="Notes..." style="width:100px"></td><td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button> <button onclick="saveNote('${cust.id}')">Save</button></td>`;});h+='</table>';document.getElementById('customerTable').innerHTML=h;}
async function saveNote(id){const note=document.getElementById('note_'+id).value;await fetch('/api/customers/'+id+'/note',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({notes:note})});alert('Note saved!');}
async function loadAppointments(){const r=await fetch('/api/appointments');const a=await r.json();let p='',c='',comp='',can='';a.forEach(app=>{const actions=`<div><button class="btn-confirm" onclick="updateStatus('${app.id}','confirmed')">✅</button><button class="btn-complete" onclick="updateStatus('${app.id}','completed')">⭐</button><button class="btn-cancel" onclick="cancelAppointment('${app.id}')">❌</button><button class="btn-delete" onclick="deleteAppointment('${app.id}')">🗑️</button></div>`;const card=`<div class="status-${app.status} appt-card"><div><strong>${app.customer_name}</strong> - ${app.service}<br>📅 ${app.datetime}</div>${actions}</div>`;if(app.status==='pending')p+=card;else if(app.status==='confirmed')c+=card;else if(app.status==='completed')comp+=card;else if(app.status==='cancelled')can+=card;});document.getElementById('pendingList').innerHTML=p||'<p>No pending</p>';document.getElementById('confirmedList').innerHTML=c||'<p>No confirmed</p>';document.getElementById('completedList').innerHTML=comp||'<p>No completed</p>';document.getElementById('cancelledList').innerHTML=can||'<p>No cancelled</p>';}
async function updateStatus(id,status){await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status})});loadAppointments();loadDashboard();}
async function cancelAppointment(id){if(confirm('Cancel?')){await fetch('/api/appointments/'+id+'/cancel',{method:'PUT'});loadAppointments();loadDashboard();}}
async function deleteAppointment(id){if(confirm('Delete?')){await fetch('/api/appointments/'+id,{method:'DELETE'});loadAppointments();loadDashboard();}}
function filterApps(status){document.querySelectorAll('.appt-tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');document.querySelectorAll('.appointment-list').forEach(l=>l.classList.remove('active'));document.getElementById(status+'List').classList.add('active');}
async function loadServices(){const r=await fetch('/api/services');const s=await r.json();let h='<table><tr><th>Name</th><th>Price</th><th>Category</th><th>Material</th><th>Action</th></tr>';s.forEach(serv=>{h+=`<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.category}</td><td>$${serv.material_cost||0}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td></tr>`;});h+='</table>';document.getElementById('serviceTable').innerHTML=h;}
async function addService(){await fetch('/api/services',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('newName').value,price:parseInt(document.getElementById('newPrice').value),duration:60,category:document.getElementById('newCat').value,material_cost:parseInt(document.getElementById('newCost').value)||0})});loadServices();}
async function deleteService(id){if(confirm('Delete?')){await fetch('/api/services/'+id,{method:'DELETE'});loadServices();}}
async function deleteCustomer(id){if(confirm('Delete?')){await fetch('/api/customers/'+id,{method:'DELETE'});loadCustomers();loadDashboard();}}
async function loadMaterials(){const r=await fetch('/api/materials');const d=await r.json();let h='<table><tr><th>Category</th><th>Cost</th><th>Items</th><th>Action</th></tr>';for(let cat in d.materials){h+=`<tr><td>${cat}</td><td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:70px"> $</td><td>${d.materials[cat].items.join(', ')}</td><td><button onclick="updateCost('${cat}')">Update</button></td></tr>`;}h+='</table>';document.getElementById('materialsGrid').innerHTML=h;document.getElementById('profitSummary').innerHTML=`<h3>Financial Summary</h3><p>Revenue: $${d.totalRevenue} | Materials: $${d.totalMaterialCost} | Net: $${d.netProfit}</p>`;}
async function updateCost(cat){const cost=document.getElementById('cost_'+cat).value;await fetch('/api/materials/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat,cost:parseInt(cost)})});loadMaterials();}
async function askAI(){const q=document.getElementById('aiQuestion').value;if(!q)return;const r=await fetch('/api/ai/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();document.getElementById('aiResponse').innerHTML=d.answer;}
let lastCount=0;
async function loadNotif(){const r=await fetch('/api/notifications');const n=await r.json();const b=document.getElementById('bellBadge');if(n.length>0){b.style.display='flex';b.innerText=n.length;}else{b.style.display='none';}let h='';n.forEach(not=>{h+=`<div class="notif-item">🔔 ${not.message}<div style="font-size:10px;">${not.time}</div></div>`;});document.getElementById('notifList').innerHTML=h||'<div>No notifications</div>';if(n.length>lastCount&&lastCount>0){document.querySelector('.floating-bell').style.transform='scale(1.2)';setTimeout(()=>document.querySelector('.floating-bell').style.transform='scale(1)',300);}lastCount=n.length;}
function toggleNotif(){const p=document.getElementById('notifPopup');p.classList.toggle('show');if(p.classList.contains('show'))loadNotif();}
loadDashboard();loadNotif();setInterval(()=>{if(document.getElementById('dashboard').classList.contains('active'))loadDashboard();loadNotif();},15000);
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
    if 'nail' in q: a = "💅 Gel $35, Acrylic $40, Manicure $10"
    elif 'lash' in q: a = "👁️ Classic $35, Volume $38, Mega $45"
    elif 'skin' in q: a = "💆 Facials $35-65, Mesotherapy $35-100"
    elif 'wax' in q: a = "🕯️ Full body $45, Bikini $23, Legs $17"
    elif 'price' in q: a = "💰 Nails $10-40, Lashes $35-45, Skincare $35-200, Wax $3-45"
    else: a = "✨ Medical Touch: Nails, Lashes, Skincare, Wax. Ask anything!"
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
        cust = {'id': str(len(data['customers']) + 1), 'name': b['name'], 'phone': b['phone'], 'email': b.get('email', ''), 'visits': 0, 'notes': ''}
        data['customers'].append(cust)
    appt = {'id': str(len(data['appointments']) + 1), 'customer_id': cust['id'], 'customer_name': cust['name'], 'service': b['service'], 'datetime': b['datetime'], 'status': 'pending', 'staff_id': 'staff1', 'booked_at': datetime.now().isoformat()}
    data['appointments'].append(appt)
    save_data(data)
    add_notification(f"📅 NEW: {cust['name']} booked {b['service']}")
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
    return jsonify({'success': True})

@app.route('/api/appointments/<appointment_id>/cancel', methods=['PUT'])
def cancel_appointment(appointment_id):
    data = load_data()
    for a in data['appointments']:
        if a['id'] == appointment_id:
            a['status'] = 'cancelled'
            add_notification(f"❌ Cancelled: {a['customer_name']}")
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
                add_notification(f"✅ Completed: {a['customer_name']}")
            elif status == 'confirmed':
                add_notification(f"📌 Confirmed: {a['customer_name']}")
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
    return jsonify({'materials': data.get('materials'), 'totalRevenue': rev, 'totalMaterialCost': mat, 'netProfit': rev - mat})

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
                except: pass
    popular = []
    for name in pop:
        popular.append({'name': name, 'count': pop[name], 'revenue': pop_rev.get(name, 0), 'netProfit': pop_rev.get(name, 0) - pop_mat.get(name, 0)})
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
            {'title': 'Customers', 'value': len(data['customers'])},
            {'title': 'Appointments', 'value': len(apps)},
            {'title': 'Pending', 'value': sum(1 for a in apps if a.get('status') == 'pending')},
            {'title': 'Completed', 'value': sum(1 for a in apps if a.get('status') == 'completed')}
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
    total = sum(services.get(a['service'], {}).get('price', 0) for a in apps if a.get('status') == 'completed')
    materials = sum(services.get(a['service'], {}).get('material_cost', 0) for a in apps if a.get('status') == 'completed')
    net = total - materials
    if 'profit' in q: a = f"💰 Revenue: ${total}, Materials: ${materials}, Net: ${net}. Margin: {((net/total)*100) if total>0 else 0:.1f}%"
    elif 'predict' in q: a = f"📈 Next month projection: ${(total/12)*1.15:.2f} if you maintain current pace"
    else: a = f"💡 You have {len(data['customers'])} customers, ${net} net profit. Ask about profits or predictions!"
    return jsonify({'answer': a})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✨ MEDICAL TOUCH CRM v3.0 - WORKING! ✨")
    print("="*60)
    print("\n📍 CUSTOMER: https://medical-touch.onrender.com")
    print("🔐 ADMIN: https://medical-touch.onrender.com/admin")
    print("\n🔑 Admin Login: medicaltouch / admin123")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
