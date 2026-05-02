from flask import Flask, render_template_string, request, jsonify, send_from_directory, session, redirect, url_for
import json
import os
from datetime import datetime
import time
from functools import wraps
from collections import Counter

app = Flask(__name__)
app.secret_key = 'medicaltouchsecretkey2024'

# Use environment variable for data path (Render persistent disk)
DATA_DIR = os.environ.get('DATA_DIR', '.')
DATA_FILE = os.path.join(DATA_DIR, 'salon_data.json')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')

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
    # Initialize with default data
    default_data = {
        'customers': [],
        'appointments': [],
        'cancelled_appointments': [],
        'materials': {
            'Nails': {'cost': 500, 'items': ['Gel Polish', 'Acrylic Powder', 'Tips', 'Files']},
            'Lashes': {'cost': 300, 'items': ['Lash Glue', 'Lashes', 'Tweezers', 'Primer']},
            'Skincare': {'cost': 400, 'items': ['Serums', 'Masks', 'MesoNeedles', 'Products']},
            'Wax': {'cost': 200, 'items': ['Wax Beans', 'Strips', 'Oil', 'Pre/Post Care']}
        },
        'services': [
            {'id': '1', 'name': 'Full Set GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5},
            {'id': '2', 'name': 'Full Set Fiber GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5},
            {'id': '3', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '4', 'name': 'Facial Classic', 'price': 35, 'duration': 60, 'category': 'Skincare', 'material_cost': 4},
            {'id': '5', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax', 'material_cost': 3},
        ]
    }
    # Add more default services
    for i in range(6, 61):
        default_data['services'].append({'id': str(i), 'name': f'Service {i}', 'price': 30, 'duration': 60, 'category': 'Nails', 'material_cost': 3})
    save_data(default_data)
    return default_data

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
.address{background:#ff6b9d;display:inline-block;padding:10px 30px;border-radius:50px;margin-top:15px;font-size:14px;}
.search-bar{max-width:500px;margin:20px auto 0;}
.search-bar input{width:100%;padding:14px 20px;border:2px solid #ff6b9d;border-radius:50px;font-size:16px;background:white;}
.tabs{display:flex;justify-content:center;gap:8px;background:white;padding:12px;position:sticky;top:0;flex-wrap:wrap;}
.tab{padding:10px 28px;font-size:15px;font-weight:500;background:none;border:none;cursor:pointer;border-radius:40px;color:#666;}
.tab:hover{background:#ff6b9d20;color:#ff6b9d;}
.tab.active{background:#ff6b9d;color:white;}
.container{max-width:1300px;margin:0 auto;padding:40px 20px;}
.tab-content{display:none;animation:fadeIn 0.4s ease;}
.tab-content.active{display:block;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:25px;margin-top:30px;}
.service-card{background:white;border-radius:20px;padding:22px;cursor:pointer;transition:0.3s;border:1px solid #eee;}
.service-card:hover{transform:translateY(-5px);border-color:#ff6b9d;}
.service-name{font-size:16px;font-weight:600;color:#1a1a2e;margin-bottom:8px;}
.service-price{font-size:26px;font-weight:bold;color:#ff6b9d;}
.service-duration{color:#aaa;font-size:12px;margin-top:8px;}
.booking-section{background:linear-gradient(135deg,#fff5f7,#ffe4e8);border-radius:28px;padding:45px;margin-top:20px;}
.booking-section h2{font-family:'Playfair Display',serif;font-size:32px;color:#1a1a2e;margin-bottom:25px;}
.form-group{margin-bottom:20px;}
input,select{width:100%;padding:14px;border:2px solid #eee;border-radius:14px;font-size:15px;}
input:focus,select:focus{outline:none;border-color:#ff6b9d;}
.submit-btn{background:#ff6b9d;color:white;border:none;padding:14px;border-radius:40px;font-size:16px;font-weight:bold;cursor:pointer;width:100%;}
.warning{color:#ff4d7d;font-size:12px;margin-top:5px;display:none;}
footer{background:#1a1a2e;color:white;text-align:center;padding:40px;margin-top:60px;}
.chat-btn{position:fixed;bottom:30px;right:30px;width:65px;height:65px;background:linear-gradient(135deg,#ff6b9d,#ff4d7d);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:30px;z-index:1000;}
.chat-window{position:fixed;bottom:110px;right:30px;width:350px;height:480px;background:white;border-radius:20px;display:none;flex-direction:column;z-index:1000;box-shadow:0 10px 40px rgba(0,0,0,0.2);}
.chat-window.show{display:flex;}
.chat-header{background:linear-gradient(135deg,#ff6b9d,#ff4d7d);color:white;padding:15px;border-radius:20px 20px 0 0;}
.chat-messages{flex:1;overflow-y:auto;padding:15px;background:#f5f5f5;}
.bot-msg{background:white;padding:10px 15px;border-radius:18px;margin:8px 0;max-width:85%;}
.user-msg{background:#ff6b9d;color:white;padding:10px 15px;border-radius:18px;margin:8px 0;max-width:85%;margin-left:auto;}
.chat-input{display:flex;padding:12px;border-top:1px solid #ddd;}
.chat-input input{flex:1;padding:12px;margin:0;margin-right:10px;border:1px solid #ddd;border-radius:25px;}
.chat-input button{background:#ff6b9d;color:white;border:none;border-radius:25px;padding:12px 20px;cursor:pointer;}
.no-results{text-align:center;color:#999;padding:40px;}
@media(max-width:768px){.hero h1{font-size:32px;}.tab{padding:8px 18px;}}
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
<footer><p>✨ Medical Touch - Where Beauty Meets Medical Excellence ✨<br>📍 Bakaata - Ain W ZEIN Road | 📞 81023625</p></footer>
<div class="chat-btn" onclick="toggleChat()">💬</div>
<div class="chat-window" id="chatWindow">
<div class="chat-header">🤖 Medical Touch AI Assistant</div>
<div class="chat-messages" id="chatMsgs">
<div class="bot-msg">Hello! Ask me about nails, lashes, skincare, wax, or prices!</div>
</div>
<div class="chat-input"><input type="text" id="chatInput" placeholder="Ask me..." onkeypress="if(event.key==='Enter')sendChat()"><button onclick="sendChat()">Send</button></div>
</div>
<script>
let allServices = [];
fetch('/api/services').then(r=>r.json()).then(services => { allServices = services; displayServices(services); populateSelect(services); });
function displayServices(services){
const cats = {'Nails':'nailsGrid','Lashes':'lashesGrid','Skincare':'skincareGrid','Wax':'waxGrid'};
for(let [cat, elId] of Object.entries(cats)){
let filtered = services.filter(s => s.category === cat);
let html = '';
filtered.forEach(s => { html += `<div class="service-card" onclick="bookService('${s.name}')"><div class="service-name">${s.name}</div><div class="service-price">$${s.price}</div><div class="service-duration">⏱️ ${s.duration} min</div><div style="color:#ff6b9d;margin-top:10px;">Click to book →</div></div>`; });
document.getElementById(elId).innerHTML = html || '<p>Loading...</p>';
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
}}
function populateSelect(services){
let html = '<option value="">Select Service</option>';
services.forEach(s => { html += `<option value="${s.name}">${s.name} - $${s.price}</option>`; });
document.getElementById('serviceSelect').innerHTML = html;
}
function bookService(name){ document.getElementById('serviceSelect').value = name; switchTab('book'); }
function switchTab(tab){
document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
event.target.classList.add('active');
document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
document.getElementById(tab).classList.add('active');
}
document.getElementById('appointmentDate').onchange = async function() {
const res = await fetch('/api/check-slot', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({datetime:this.value})});
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
const res = await fetch('/api/customer-book', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
const result = await res.json();
if(result.success) alert('✅ Appointment booked! We will confirm via SMS.');
else if(result.double_booking) alert('❌ Sorry, this time is already taken.');
else alert('❌ Error. Please try again.');
if(result.success) document.getElementById('bookingForm').reset();
};
function toggleChat(){ document.getElementById('chatWindow').classList.toggle('show'); }
async function sendChat(){
const input = document.getElementById('chatInput');
const q = input.value.trim(); if(!q) return;
const msgs = document.getElementById('chatMsgs');
msgs.innerHTML += `<div class="user-msg">${q}</div>`;
input.value = '';
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
.sidebar{width:270px;background:#1a1a2e;color:white;position:fixed;height:100%;padding:30px 20px;overflow-y:auto;}
.sidebar h2{font-size:22px;margin-bottom:40px;text-align:center;}
.sidebar nav a{display:block;color:white;padding:12px 18px;margin:8px 0;border-radius:12px;cursor:pointer;}
.sidebar nav a:hover{background:#ff6b9d;}
.main{margin-left:270px;padding:25px;}
.top-bar{background:white;padding:15px 25px;border-radius:15px;margin-bottom:25px;display:flex;justify-content:space-between;}
.logout-btn{background:#ff4d7d;color:white;border:none;padding:10px 20px;border-radius:30px;cursor:pointer;}
.wheels-container{display:grid;grid-template-columns:1fr 1fr;gap:25px;margin-bottom:30px;}
.wheel-card{background:white;border-radius:20px;padding:25px;text-align:center;}
.wheel{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;}
.wheel-item{width:110px;height:110px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;cursor:pointer;}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:30px;}
.stat-card{background:white;border-radius:15px;padding:20px;text-align:center;}
.stat-card .number{font-size:32px;font-weight:bold;color:#ff6b9d;}
.section{background:white;border-radius:20px;padding:25px;margin-bottom:25px;display:none;}
.section.active{display:block;}
.section h2{color:#1a1a2e;margin-bottom:20px;}
.appointment-tabs{display:flex;gap:10px;margin-bottom:20px;border-bottom:2px solid #eee;flex-wrap:wrap;}
.appt-tab{padding:12px 24px;cursor:pointer;border:none;background:none;font-weight:600;border-radius:30px;transition:0.3s;}
.appt-tab:hover{background:#f0f0f0;}
.appt-tab.active{background:#ff6b9d;color:white;}
.appointment-list{display:none;}
.appointment-list.active{display:block;}
.appt-card{padding:15px;margin:10px 0;border-radius:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;}
.status-pending{background:linear-gradient(135deg,#fff5f5,#ffe0e0);border-left:4px solid #dc3545;}
.status-confirmed{background:linear-gradient(135deg,#f0fff4,#d4f5e0);border-left:4px solid #28a745;}
.status-completed{background:linear-gradient(135deg,#e8f4fd,#d0e8f5);border-left:4px solid #007bff;}
.status-cancelled{background:#f8f9fa;border-left:4px solid #6c757d;opacity:0.7;}
.appt-info{flex:1;}
.appt-actions{display:flex;gap:8px;}
.btn-confirm{background:#28a745;color:white;border:none;padding:6px 12px;border-radius:8px;cursor:pointer;}
.btn-complete{background:#007bff;color:white;border:none;padding:6px 12px;border-radius:8px;cursor:pointer;}
.btn-cancel{background:#ffc107;color:#333;border:none;padding:6px 12px;border-radius:8px;cursor:pointer;}
.btn-delete{background:#dc3545;color:white;border:none;padding:6px 12px;border-radius:8px;cursor:pointer;}
.notes-input{width:100%;padding:8px;margin-top:5px;border:1px solid #ddd;border-radius:8px;font-size:12px;}
table{width:100%;border-collapse:collapse;}
th,td{padding:12px;text-align:left;border-bottom:1px solid #eee;}
th{background:#fef8f9;color:#ff6b9d;}
input,select{padding:8px;margin:5px;border:1px solid #ddd;border-radius:6px;}
button{background:#ff6b9d;color:white;border:none;padding:8px 15px;border-radius:6px;cursor:pointer;}
.ai-box{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:20px;padding:25px;color:white;}
.ai-box input{width:60%;padding:10px;}
.floating-bell{position:fixed;bottom:30px;right:30px;width:55px;height:55px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:25px;box-shadow:0 5px 15px rgba(0,0,0,0.2);}
.bell-badge{position:absolute;top:-5px;right:-5px;background:#dc3545;border-radius:50%;width:18px;height:18px;font-size:10px;display:flex;align-items:center;justify-content:center;}
.notif-popup{position:fixed;bottom:100px;right:30px;width:300px;background:white;border-radius:12px;display:none;box-shadow:0 5px 15px rgba(0,0,0,0.2);z-index:1000;}
.notif-popup.show{display:block;}
.notif-header{background:#ff6b9d;color:white;padding:10px;border-radius:12px 12px 0 0;}
.notif-item{padding:10px;border-bottom:1px solid #eee;font-size:12px;}
.profit-detail{margin-top:15px;padding:10px;background:#fef8f9;border-radius:10px;display:none;}
@media(max-width:768px){.sidebar{width:100%;height:auto;position:relative;}.main{margin-left:0;}.stats-grid{grid-template-columns:1fr 1fr;}}
</style>
</head>
<body>
<div class="sidebar"><h2>💅 MEDICAL TOUCH</h2><nav><a onclick="showSection('dashboard')">📊 Dashboard</a><a onclick="showSection('customers')">👥 Customers</a><a onclick="showSection('appointments')">📅 Appointments</a><a onclick="showSection('services')">💅 Services</a><a onclick="showSection('materials')">📦 Materials</a><a onclick="showSection('ai')">🤖 AI</a></nav></div>
<div class="main">
<div class="top-bar"><h2>Admin Dashboard</h2><button class="logout-btn" onclick="location.href='/admin/logout'">Logout</button></div>
<div id="dashboard" class="section active">
<div class="wheels-container"><div class="wheel-card"><h3>💰 Profit Wheels</h3><div class="wheel"><div class="wheel-item" style="background:#1a1a2e" onclick="showProfit('today')"><span id="todayAmt">$0</span><div>Today</div></div><div class="wheel-item" style="background:#ff6b9d" onclick="showProfit('week')"><span id="weekAmt">$0</span><div>Week</div></div><div class="wheel-item" style="background:#ff4d7d" onclick="showProfit('month')"><span id="monthAmt">$0</span><div>Month</div></div><div class="wheel-item" style="background:#1a1a2e" onclick="showProfit('year')"><span id="yearAmt">$0</span><div>Year</div></div></div><div id="profitDetail" class="profit-detail"></div></div><div class="wheel-card"><h3>🎯 Most Wanted Services</h3><div id="popularWheel" class="wheel"></div><div id="popularDetail" class="profit-detail"></div></div></div>
<div class="stats-grid" id="statsGrid"></div>
<h3>Recent Bookings</h3><div id="recentList"></div>
</div>
<div id="customers" class="section"><h2>Customers with Notes</h2><div id="customerTable"></div></div>
<div id="appointments" class="section"><h2>📅 Appointment Manager</h2><div class="appointment-tabs"><button class="appt-tab active" onclick="filterAppointments('pending')">⏳ Pending</button><button class="appt-tab" onclick="filterAppointments('confirmed')">✅ Confirmed</button><button class="appt-tab" onclick="filterAppointments('completed')">⭐ Completed</button><button class="appt-tab" onclick="filterAppointments('cancelled')">❌ Cancelled</button></div><div id="pendingList" class="appointment-list active"></div><div id="confirmedList" class="appointment-list"></div><div id="completedList" class="appointment-list"></div><div id="cancelledList" class="appointment-list"></div></div>
<div id="services" class="section"><h2>Services</h2><div><input type="text" id="newName" placeholder="Service Name"><input type="number" id="newPrice" placeholder="Price"><select id="newCat"><option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option></select><input type="number" id="newCost" placeholder="Material Cost"><button onclick="addService()">Add</button></div><div id="serviceTable"></div></div>
<div id="materials" class="section"><h2>Materials & Costs</h2><div id="materialsGrid"></div><div id="profitSummary"></div></div>
<div id="ai" class="section"><div class="ai-box"><h2>🤖 AI Assistant</h2><p>Ask about profits or predictions</p><input type="text" id="aiQuestion" placeholder="How much profit?"><button onclick="askAI()">Ask</button><div id="aiResponse" class="ai-response"></div></div></div>
</div>
<div class="floating-bell" onclick="toggleNotif()">🔔<span id="bellBadge" class="bell-badge" style="display:none;">0</span></div>
<div id="notifPopup" class="notif-popup"><div class="notif-header">Notifications</div><div id="notifList"></div></div>
<script>
let profitData={}, popularData=[];
function showSection(s){document.querySelectorAll('.section').forEach(sec=>sec.classList.remove('active'));document.getElementById(s).classList.add('active');if(s==='dashboard')loadDashboard();if(s==='customers')loadCustomers();if(s==='appointments')loadAppointments();if(s==='services')loadServices();if(s==='materials')loadMaterials();}
async function loadDashboard(){const r=await fetch('/api/admin/stats');const d=await r.json();profitData=d.profit;popularData=d.popular;document.getElementById('todayAmt').innerText='$'+profitData.today;document.getElementById('weekAmt').innerText='$'+profitData.week;document.getElementById('monthAmt').innerText='$'+profitData.month;document.getElementById('yearAmt').innerText='$'+profitData.year;let s='';d.stats.forEach(st=>{s+=`<div class="stat-card"><div class="number">${st.value}</div><p>${st.title}</p></div>`;});document.getElementById('statsGrid').innerHTML=s;let pHtml='';const cols=['#ff6b9d','#ff4d7d','#ffb347','#4ecdc4','#45b7d1','#96ceb4'];popularData.forEach((p,i)=>{pHtml+=`<div class="wheel-item" style="background:${cols[i%cols.length]}" onclick="showPopular('${p.name}')"><span>${p.name.length>8?p.name.substring(0,6):p.name}</span><div>${p.count} 📅</div><div style="font-size:11px">💰 $${p.revenue}</div></div>`;});document.getElementById('popularWheel').innerHTML=pHtml||'<p>No data</p>';let rHtml='';d.recent.forEach(a=>{let statusClass='';if(a.status==='pending')statusClass='status-pending';else if(a.status==='confirmed')statusClass='status-confirmed';else if(a.status==='completed')statusClass='status-completed';else statusClass='status-cancelled';rHtml+=`<div class="${statusClass} appt-card"><div class="appt-info"><strong>${a.customer_name}</strong> - ${a.service}<br>📅 ${a.datetime}</div></div>`;});document.getElementById('recentList').innerHTML=rHtml||'<p>No appointments</p>';}
function showProfit(p){const d=document.getElementById('profitDetail');let msg='';if(p==='today')msg=`💰 Today: $${profitData.today} (${profitData.todayCount||0} appts) | Net: $${profitData.todayNet||0}`;if(p==='week')msg=`💰 Week: $${profitData.week} (${profitData.weekCount||0} appts) | Net: $${profitData.weekNet||0}`;if(p==='month')msg=`💰 Month: $${profitData.month} (${profitData.monthCount||0} appts) | Net: $${profitData.monthNet||0}`;if(p==='year')msg=`💰 Year: $${profitData.year} (${profitData.yearCount||0} appts) | Net: $${profitData.yearNet||0}`;d.innerHTML=msg;d.style.display='block';setTimeout(()=>d.style.display='none',4000);}
function showPopular(n){const d=document.getElementById('popularDetail');const p=popularData.find(x=>x.name===n);if(p)d.innerHTML=`🎯 ${p.name}: ${p.count} bookings | Revenue: $${p.revenue} | Net: $${p.netProfit}`;d.style.display='block';setTimeout(()=>d.style.display='none',4000);}
async function loadCustomers(){const r=await fetch('/api/customers');const c=await r.json();let h='<table><tr><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Notes</th><th>Action</th></tr>';c.forEach(cust=>{h+=`<tr><td>${cust.name}</td><td>${cust.phone}</td><td>${cust.email||'-'}</td><td>${cust.visits||0}</td><td><input class="notes-input" type="text" id="note_${cust.id}" value="${cust.notes||''}" placeholder="Add notes..."></td><td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button> <button onclick="saveNote('${cust.id}')">Save Note</button></td></tr>`;});h+='</table>';document.getElementById('customerTable').innerHTML=h;}
async function saveNote(id){const note=document.getElementById('note_'+id).value;await fetch('/api/customers/'+id+'/note',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({notes:note})});alert('Note saved!');}
async function loadAppointments(){const r=await fetch('/api/appointments');const a=await r.json();let pending='',confirmed='',completed='',cancelled='';a.forEach(app=>{const actions=`<div class="appt-actions">${app.status==='pending'?`<button class="btn-confirm" onclick="updateStatus('${app.id}','confirmed')">✅ Confirm</button>`:''}${app.status==='pending'||app.status==='confirmed'?`<button class="btn-complete" onclick="updateStatus('${app.id}','completed')">⭐ Complete</button>`:''}<button class="btn-cancel" onclick="cancelAppointment('${app.id}')">❌ Cancel</button><button class="btn-delete" onclick="deleteAppointment('${app.id}')">🗑️ Delete</button></div>`;const card=`<div class="status-${app.status} appt-card"><div class="appt-info"><strong>${app.customer_name}</strong> - ${app.service}<br>📅 ${app.datetime}<br>Status: ${app.status}</div>${actions}</div>`;if(app.status==='pending')pending+=card;else if(app.status==='confirmed')confirmed+=card;else if(app.status==='completed')completed+=card;else if(app.status==='cancelled')cancelled+=card;});document.getElementById('pendingList').innerHTML=pending||'<p>No pending appointments</p>';document.getElementById('confirmedList').innerHTML=confirmed||'<p>No confirmed appointments</p>';document.getElementById('completedList').innerHTML=completed||'<p>No completed appointments</p>';document.getElementById('cancelledList').innerHTML=cancelled||'<p>No cancelled appointments</p>';}
async function updateStatus(id,status){await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:status})});loadAppointments();loadDashboard();}
async function cancelAppointment(id){if(confirm('Cancel this appointment?')){await fetch('/api/appointments/'+id+'/cancel',{method:'PUT'});loadAppointments();loadDashboard();}}
async function deleteAppointment(id){if(confirm('Permanently delete this appointment?')){await fetch('/api/appointments/'+id,{method:'DELETE'});loadAppointments();loadDashboard();}}
function filterAppointments(status){document.querySelectorAll('.appt-tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');document.querySelectorAll('.appointment-list').forEach(list=>list.classList.remove('active'));document.getElementById(status+'List').classList.add('active');}
async function loadServices(){const r=await fetch('/api/services');const s=await r.json();let h='<table><th>Name</th><th>Price</th><th>Duration</th><th>Category</th><th>Material</th><th>Action</th></tr>';s.forEach(serv=>{h+=`<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.duration}min</td><td>${serv.category}</td><td>$${serv.material_cost||0}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td></tr>`;});h+='</table>';document.getElementById('serviceTable').innerHTML=h;}
async function addService(){await fetch('/api/services',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('newName').value,price:parseInt(document.getElementById('newPrice').value),duration:60,category:document.getElementById('newCat').value,material_cost:parseInt(document.getElementById('newCost').value)||0})});loadServices();}
async function deleteService(id){if(confirm('Delete?')){await fetch('/api/services/'+id,{method:'DELETE'});loadServices();}}
async function deleteCustomer(id){if(confirm('Delete?')){await fetch('/api/customers/'+id,{method:'DELETE'});loadCustomers();}}
async function loadMaterials(){const r=await fetch('/api/materials');const d=await r.json();let h='<table><th>Category</th><th>Cost</th><th>Items</th><th>Action</th></tr>';for(let cat in d.materials){h+=`<tr><td><strong>${cat}</strong></td><td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:80px"> $</td><td>${d.materials[cat].items.join(', ')}</td><td><button onclick="updateCost('${cat}')">Update</button></td></tr>`;}h+='</table>';document.getElementById('materialsGrid').innerHTML=h;document.getElementById('profitSummary').innerHTML=`<h3>Financial Summary</h3><p>Revenue: $${d.totalRevenue} | Materials: $${d.totalMaterialCost} | Net: $${d.netProfit}</p>`;}
async function updateCost(cat){const cost=document.getElementById('cost_'+cat).value;await fetch('/api/materials/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat,cost:parseInt(cost)})});loadMaterials();}
async function askAI(){const q=document.getElementById('aiQuestion').value;if(!q)return;const r=await fetch('/api/ai/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();document.getElementById('aiResponse').innerHTML=d.answer;document.getElementById('aiResponse').style.display='block';}
let lastCount=0;
async function loadNotif(){const r=await fetch('/api/notifications');const n=await r.json();const b=document.getElementById('bellBadge');if(n.length>0){b.style.display='flex';b.innerText=n.length;}else{b.style.display='none';}let h='';n.forEach(not=>{h+=`<div class="notif-item">🔔 ${not.message}<div style="font-size:10px;color:#999;">${not.time}</div></div>`;});document.getElementById('notifList').innerHTML=h||'<div>No notifications</div>';if(n.length>lastCount&&lastCount>0){document.querySelector('.floating-bell').style.transform='scale(1.2)';setTimeout(()=>document.querySelector('.floating-bell').style.transform='scale(1)',300);}lastCount=n.length;}
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
    if 'nail' in q: a = "💅 Gel $35, Acrylic $40, Manicure $10, Pedicure $15"
    elif 'lash' in q: a = "👁️ Classic $35, Volume $38, Mega $45, Refill $25"
    elif 'skin' in q: a = "💆 Facials $35-65, Mesotherapy $35-100, HIFU $100"
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
    add_notification(f"📅 NEW: {cust['name']} booked {b['service']} at {b['datetime']}")
    return jsonify({'success': True})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(load_data()['customers'])

@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    data = load_data()
    data['customers'] = [c for c in data['customers'] if c['id'] != customer_id]
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
            add_notification(f"❌ Cancelled: {a['customer_name']} - {a['service']}")
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
                add_notification(f"✅ Completed: {a['customer_name']} - {a['service']}")
            elif status == 'confirmed':
                add_notification(f"📌 Confirmed: {a['customer_name']} - {a['service']}")
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
                except: pass
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
            {'title': '👥 Customers', 'value': len(data['customers'])},
            {'title': '📅 Appointments', 'value': len(apps)},
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
    elif 'predict' in q:
        a = f"📈 Next month projection: ${(total/12)*1.15:.2f} if you maintain current pace"
    else:
        a = f"💡 You have {len(data['customers'])} customers, {len(apps)} appointments, ${net} net profit"
    return jsonify({'answer': a})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✨ MEDICAL TOUCH CRM v3.0 - FULLY UPGRADED! ✨")
    print("="*60)
    print("\n📍 CUSTOMER: https://medical-touch.onrender.com")
    print("🔐 ADMIN: https://medical-touch.onrender.com/admin")
    print("\n🔑 Admin Login: medicaltouch / admin123")
    print("\n✅ NEW FEATURES ADDED:")
    print("   • 🔍 Search bar for services")
    print("   • 🎨 Beautiful colored appointment tabs with action buttons")
    print("   • ✅ Confirm button to accept pending appointments")
    print("   • ⭐ Complete button to finish appointments")
    print("   • ❌ Cancel button to cancel appointments")
    print("   • 🗑️ Delete button to remove appointments permanently")
    print("   • 📝 Customer notes saved")
    print("   • 💰 Most Wanted shows money now")
    print("   • 💾 Data now stays safe on updates!")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
