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
            'Skincare': {'cost': 400, 'items': ['Serums', 'Masks', 'MesoNeedles']},
            'Wax': {'cost': 200, 'items': ['Wax Beans', 'Strips', 'Oil']}
        },
        'services': [
            {'id': '1', 'name': 'Full Set GEL + Color Gel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 5},
            {'id': '2', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '3', 'name': 'Facial Classic', 'price': 35, 'duration': 60, 'category': 'Skincare', 'material_cost': 4},
            {'id': '4', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax', 'material_cost': 3},
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
    notifs.insert(0, {'id': str(int(time.time())), 'message': message, 'time': datetime.now().strftime('%I:%M %p'), 'read': False})
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
<head><title>Medical Touch Admin</title><style>
body{font-family:Poppins;background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;}
.login-box{background:white;padding:40px;border-radius:24px;width:380px;text-align:center;}
input{width:100%;padding:14px;margin:10px 0;border:2px solid #eee;border-radius:12px;}
button{background:#ff6b9d;color:white;padding:14px;border:none;border-radius:12px;width:100%;cursor:pointer;}
</style></head>
<body><div class="login-box"><h2>Medical Touch Admin</h2>
<form method="POST"><input type="text" name="username" placeholder="Username" required><input type="password" name="password" placeholder="Password" required><button type="submit">Login</button></form>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}</div></body></html>
'''

CUSTOMER_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Medical Touch</title><meta name="viewport" content="width=device-width, initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Poppins',sans-serif;background:#faf8f9;}
.hero{background:#1a1a2e;color:white;padding:50px 20px;text-align:center;}
.hero h1{font-size:42px;}
.address{background:#ff6b9d;display:inline-block;padding:8px 25px;border-radius:50px;margin-top:15px;}
.tabs{display:flex;justify-content:center;gap:8px;background:white;padding:12px;position:sticky;top:0;}
.tab{padding:10px 25px;border:none;border-radius:40px;cursor:pointer;color:#666;background:none;}
.tab.active{background:#ff6b9d;color:white;}
.container{padding:40px 20px;max-width:1300px;margin:0 auto;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin-top:20px;}
.service-card{background:white;border-radius:16px;padding:20px;cursor:pointer;border:1px solid #eee;}
.service-name{font-weight:600;margin-bottom:8px;}
.service-price{font-size:24px;font-weight:bold;color:#ff6b9d;}
.booking-section{background:linear-gradient(135deg,#fff5f7,#ffe4e8);border-radius:28px;padding:35px;}
input,select{width:100%;padding:12px;border:2px solid #eee;border-radius:12px;margin:10px 0;}
.submit-btn{background:#ff6b9d;color:white;border:none;padding:14px;border-radius:40px;width:100%;cursor:pointer;font-weight:bold;}
footer{background:#1a1a2e;color:white;text-align:center;padding:30px;margin-top:40px;}
.chatbot-btn{position:fixed;bottom:30px;right:30px;width:60px;height:60px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:30px;box-shadow:0 5px 20px rgba(0,0,0,0.2);}
.chatbot-window{position:fixed;bottom:110px;right:30px;width:350px;height:450px;background:white;border-radius:20px;display:none;flex-direction:column;box-shadow:0 10px 40px rgba(0,0,0,0.2);}
.chatbot-window.show{display:flex;}
.chatbot-header{background:#ff6b9d;color:white;padding:12px;border-radius:20px 20px 0 0;}
.chatbot-messages{flex:1;overflow-y:auto;padding:15px;background:#f5f5f5;}
.message{padding:10px 15px;border-radius:18px;margin-bottom:10px;max-width:85%;}
.user-message{background:#ff6b9d;color:white;margin-left:auto;text-align:right;}
.bot-message{background:white;color:#333;border:1px solid #ddd;}
.chatbot-input{display:flex;padding:12px;border-top:1px solid #ddd;}
.chatbot-input input{flex:1;padding:10px;margin:0;margin-right:10px;border:1px solid #ddd;border-radius:25px;}
.chatbot-input button{background:#ff6b9d;color:white;border:none;border-radius:25px;padding:10px 15px;cursor:pointer;}
.quick-btn{background:#f0f0f0;border:none;padding:6px 12px;border-radius:20px;margin:5px;font-size:11px;cursor:pointer;}
</style>
</head>
<body>
<div class="hero"><h1>MEDICAL TOUCH</h1><p>Where Beauty Meets Medical Excellence</p><div class="address">📍 Bakaata - Ain W ZEIN Road | 📞 81023625</div></div>
<div class="tabs"><button class="tab active" onclick="switchTab('services')">💅 Services</button><button class="tab" onclick="switchTab('book')">📅 Book Now</button></div>
<div class="container">
<div id="services" class="tab-content active"><div class="services-grid" id="servicesGrid"></div></div>
<div id="book" class="tab-content"><div class="booking-section"><h2>✨ Book Your Appointment</h2>
<form id="bookingForm"><input type="text" id="custName" placeholder="Full Name" required><input type="tel" id="custPhone" placeholder="Phone" required><input type="email" id="custEmail" placeholder="Email"><select id="serviceSelect" required><option value="">Select Service</option></select><input type="datetime-local" id="appointmentDate" required><div id="slotWarning" style="color:red;font-size:12px;display:none;">⚠️ Time already booked</div><button type="submit" class="submit-btn">Confirm Booking</button></form></div></div>
</div>
<footer><p>Medical Touch | Bakaata - Ain W ZEIN Road | 81023625</p></footer>
<div class="chatbot-btn" onclick="toggleChatbot()">🤖</div>
<div class="chatbot-window" id="chatbotWindow"><div class="chatbot-header">🤖 Medical Touch AI</div><div class="chatbot-messages" id="chatMessages"><div class="message bot-message">Hello! Ask me about nails, lashes, skincare, or wax!</div><div><button class="quick-btn" onclick="sendQuick('nails')">💅 Nails</button><button class="quick-btn" onclick="sendQuick('lashes')">👁️ Lashes</button><button class="quick-btn" onclick="sendQuick('skincare')">💆 Skincare</button><button class="quick-btn" onclick="sendQuick('wax')">🕯️ Wax</button><button class="quick-btn" onclick="sendQuick('price')">💰 Prices</button></div></div><div class="chatbot-input"><input type="text" id="chatInput" placeholder="Ask me..." onkeypress="if(event.key==='Enter')sendChat()"><button onclick="sendChat()">Send</button></div></div>
<script>
let services = [];
fetch('/api/services').then(r=>r.json()).then(s=>{services=s;displayServices(s);populateSelect(s);});
function displayServices(s){let html='';s.forEach(service=>{html+=`<div class="service-card" onclick="bookService('${service.name}')"><div class="service-name">${service.name}</div><div class="service-price">$${service.price}</div><div>${service.duration} min</div><div style="color:#ff6b9d;margin-top:10px;">Click to book →</div></div>`;});document.getElementById('servicesGrid').innerHTML=html;}
function populateSelect(s){let html='<option value="">Select service</option>';s.forEach(service=>{html+=`<option value="${service.name}">${service.name} - $${service.price}</option>`;});document.getElementById('serviceSelect').innerHTML=html;}
function bookService(name){document.getElementById('serviceSelect').value=name;switchTab('book');}
function switchTab(tab){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));document.getElementById(tab).classList.add('active');}
document.getElementById('appointmentDate').onchange=async function(){const r=await fetch('/api/check-slot',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({datetime:this.value})});const d=await r.json();document.getElementById('slotWarning').style.display=d.booked?'block':'none';};
document.getElementById('bookingForm').onsubmit=async(e)=>{e.preventDefault();const data={name:document.getElementById('custName').value,phone:document.getElementById('custPhone').value,email:document.getElementById('custEmail').value,service:document.getElementById('serviceSelect').value,datetime:document.getElementById('appointmentDate').value};const r=await fetch('/api/customer-book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const res=await r.json();if(res.success)alert('✅ Booked! SMS sent.');else if(res.double_booking)alert('❌ Time taken. Choose another.');else alert('❌ Error');if(res.success)document.getElementById('bookingForm').reset();};
function toggleChatbot(){document.getElementById('chatbotWindow').classList.toggle('show');}
async function sendChat(){const input=document.getElementById('chatInput');const q=input.value.trim();if(!q)return;addMessage(q,'user');input.value='';const r=await fetch('/api/ai/customer-chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();addMessage(d.answer,'bot');}
async function sendQuick(topic){let q='';if(topic==='nails')q='Tell me about nail services';if(topic==='lashes')q='Tell me about lash services';if(topic==='skincare')q='Tell me about skincare';if(topic==='wax')q='Tell me about wax services';if(topic==='price')q='What are your prices?';addMessage(q,'user');const r=await fetch('/api/ai/customer-chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();addMessage(d.answer,'bot');}
function addMessage(t,s){const div=document.getElementById('chatMessages');const msg=document.createElement('div');msg.className=`message ${s==='user'?'user-message':'bot-message'}`;msg.innerHTML=t;div.appendChild(msg);div.scrollTop=div.scrollHeight;}
</script>
</body></html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html><head><title>Medical Touch Admin</title><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box;}body{font-family:'Poppins',sans-serif;background:#f0f2f5;}
.sidebar{width:260px;background:#1a1a2e;color:white;position:fixed;height:100%;padding:25px;}
.sidebar h2{text-align:center;margin-bottom:40px;}
.sidebar nav a{display:block;color:white;padding:12px;margin:8px 0;border-radius:10px;cursor:pointer;}
.sidebar nav a:hover{background:#ff6b9d;}
.main{margin-left:260px;padding:25px;}
.top-bar{background:white;padding:15px 25px;border-radius:15px;margin-bottom:25px;display:flex;justify-content:space-between;}
.logout-btn{background:#ff4d7d;color:white;border:none;padding:10px 20px;border-radius:30px;cursor:pointer;}
.wheels-container{display:grid;grid-template-columns:1fr 1fr;gap:25px;margin-bottom:30px;}
.wheel-card{background:white;border-radius:20px;padding:25px;text-align:center;}
.wheel{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;}
.wheel-item{width:100px;height:100px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;cursor:pointer;}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:20px;margin-bottom:30px;}
.stat-card{background:white;border-radius:15px;padding:20px;text-align:center;}
.stat-card .number{font-size:32px;font-weight:bold;color:#ff6b9d;}
.section{background:white;border-radius:20px;padding:25px;margin-bottom:25px;display:none;}
.section.active{display:block;}
table{width:100%;border-collapse:collapse;}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;}
th{background:#fef8f9;color:#ff6b9d;}
.delete-btn{background:#dc3545;color:white;border:none;padding:5px 10px;border-radius:5px;cursor:pointer;}
input,select{padding:8px;margin:5px;border:1px solid #ddd;border-radius:6px;}
button{background:#ff6b9d;color:white;border:none;padding:8px 15px;border-radius:6px;cursor:pointer;}
.ai-box{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:20px;padding:25px;color:white;}
.ai-box input{width:60%;padding:10px;}
.floating-bell{position:fixed;bottom:30px;right:30px;width:60px;height:60px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;}
.bell-badge{position:absolute;top:-5px;right:-5px;background:#dc3545;color:white;border-radius:50%;width:20px;height:20px;font-size:10px;display:flex;align-items:center;justify-content:center;}
.notif-popup{position:fixed;bottom:110px;right:30px;width:300px;background:white;border-radius:15px;display:none;box-shadow:0 5px 20px rgba(0,0,0,0.2);}
.notif-popup.show{display:block;}
.notif-header{background:#ff6b9d;color:white;padding:10px;border-radius:15px 15px 0 0;}
.notif-item{padding:10px;border-bottom:1px solid #eee;font-size:12px;}
.profit-detail{margin-top:15px;padding:10px;background:#fef8f9;border-radius:10px;display:none;}
@media(max-width:768px){.sidebar{width:100%;height:auto;position:relative;}.main{margin-left:0;}}
</style></head>
<body>
<div class="sidebar"><h2>💅 MEDICAL TOUCH</h2><nav><a onclick="showSection('dashboard')">📊 Dashboard</a><a onclick="showSection('materials')">📦 Materials</a><a onclick="showSection('customers')">👥 Customers</a><a onclick="showSection('appointments')">📅 Appointments</a><a onclick="showSection('services')">💅 Services</a><a onclick="showSection('ai')">🤖 AI</a></nav></div>
<div class="main"><div class="top-bar"><h2>Admin Dashboard</h2><button class="logout-btn" onclick="location.href='/admin/logout'">Logout</button></div>
<div id="dashboard" class="section active"><div class="wheels-container"><div class="wheel-card"><h3>💰 Profit</h3><div class="wheel"><div class="wheel-item" style="background:#1a1a2e" onclick="showProfit('today')"><span id="todayAmt">$0</span><div>Today</div></div><div class="wheel-item" style="background:#ff6b9d" onclick="showProfit('week')"><span id="weekAmt">$0</span><div>Week</div></div><div class="wheel-item" style="background:#ff4d7d" onclick="showProfit('month')"><span id="monthAmt">$0</span><div>Month</div></div><div class="wheel-item" style="background:#1a1a2e" onclick="showProfit('year')"><span id="yearAmt">$0</span><div>Year</div></div></div><div id="profitDetail" class="profit-detail"></div></div><div class="wheel-card"><h3>🎯 Most Wanted</h3><div id="popularWheel" class="wheel"></div><div id="popularDetail" class="profit-detail"></div></div></div><div class="stats-grid" id="statsGrid"></div><h3>Recent Bookings</h3><div id="recentList"></div></div>
<div id="materials" class="section"><h2>Materials</h2><div id="materialsGrid"></div><div id="profitSummary"></div></div>
<div id="customers" class="section"><h2>Customers</h2><div id="customerTable"></div></div>
<div id="appointments" class="section"><h2>Appointments</h2><div id="appointmentTable"></div></div>
<div id="services" class="section"><h2>Services</h2><div><input type="text" id="newName" placeholder="Name"><input type="number" id="newPrice" placeholder="Price"><select id="newCat"><option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option></select><input type="number" id="newCost" placeholder="Material Cost"><button onclick="addService()">Add</button></div><div id="serviceTable"></div></div>
<div id="ai" class="section"><div class="ai-box"><h2>🤖 AI Assistant</h2><p>Ask about profits or predictions</p><input type="text" id="aiQuestion" placeholder="How much profit?"><button onclick="askAI()">Ask</button><div id="aiResponse" class="ai-response"></div></div></div></div>
<div class="floating-bell" onclick="toggleNotif()">🔔<span id="bellBadge" class="bell-badge" style="display:none;">0</span></div>
<div id="notifPopup" class="notif-popup"><div class="notif-header">Notifications</div><div id="notifList"></div></div>
<script>
let profitData={},popularData=[];
function showSection(s){document.querySelectorAll('.section').forEach(sec=>sec.classList.remove('active'));document.getElementById(s).classList.add('active');if(s==='dashboard')loadDashboard();if(s==='materials')loadMaterials();if(s==='customers')loadCustomers();if(s==='appointments')loadAppointments();if(s==='services')loadServices();}
async function loadDashboard(){const r=await fetch('/api/admin/stats');const d=await r.json();profitData=d.profit;popularData=d.popular;document.getElementById('todayAmt').innerText='$'+profitData.today;document.getElementById('weekAmt').innerText='$'+profitData.week;document.getElementById('monthAmt').innerText='$'+profitData.month;document.getElementById('yearAmt').innerText='$'+profitData.year;let s='';d.stats.forEach(st=>{s+=`<div class="stat-card"><div class="number">${st.value}</div><p>${st.title}</p></div>`;});document.getElementById('statsGrid').innerHTML=s;let pHtml='';const colors=['#ff6b9d','#ff4d7d','#ffb347','#4ecdc4'];popularData.forEach((p,i)=>{pHtml+=`<div class="wheel-item" style="background:${colors[i%colors.length]}" onclick="showPopular('${p.name}')"><span>${p.name.substring(0,6)}</span><div>${p.count}</div></div>`;});document.getElementById('popularWheel').innerHTML=pHtml||'<p>No data</p>';let rHtml='';d.recent.forEach(a=>{rHtml+=`<div style="padding:10px;margin:5px 0;border-left:3px solid #ff6b9d;background:#f8f9fa;"><strong>${a.customer_name}</strong> - ${a.service}<br>${a.datetime} | ${a.status}</div>`;});document.getElementById('recentList').innerHTML=rHtml||'<p>No appointments</p>';}
function showProfit(p){const d=document.getElementById('profitDetail');let msg='';if(p==='today')msg=`💰 Today: $${profitData.today} | Net: $${profitData.todayNet||0}`;if(p==='week')msg=`💰 Week: $${profitData.week} | Net: $${profitData.weekNet||0}`;if(p==='month')msg=`💰 Month: $${profitData.month} | Net: $${profitData.monthNet||0}`;if(p==='year')msg=`💰 Year: $${profitData.year} | Net: $${profitData.yearNet||0}`;d.innerHTML=msg;d.style.display='block';setTimeout(()=>d.style.display='none',3000);}
function showPopular(n){const d=document.getElementById('popularDetail');const p=popularData.find(x=>x.name===n);if(p)d.innerHTML=`🎯 ${p.name}: ${p.count} bookings | Net: $${p.netProfit}`;d.style.display='block';setTimeout(()=>d.style.display='none',3000);}
async function loadMaterials(){const r=await fetch('/api/materials');const d=await r.json();let h='</tr><th>Category</th><th>Cost</th><th>Items</th><th>Action</th></td>';for(let cat in d.materials){h+=`<tr><td><strong>${cat}</strong></td><td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:80px"> $</td><td>${d.materials[cat].items.join(', ')}</td><td><button onclick="updateCost('${cat}')">Update</button></td></tr>`;}h+='</table>';document.getElementById('materialsGrid').innerHTML=h;document.getElementById('profitSummary').innerHTML=`<h3>Financial Summary</h3><p>Revenue: $${d.totalRevenue} | Materials: $${d.totalMaterialCost} | Net: $${d.netProfit}</p>`;}
async function updateCost(cat){const cost=document.getElementById('cost_'+cat).value;await fetch('/api/materials/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat,cost:parseInt(cost)})});loadMaterials();}
async function loadCustomers(){const r=await fetch('/api/customers');const c=await r.json();let h='<table><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Action</th></tr>';c.forEach(cust=>{h+=`<tr><td>${cust.name}</td><td>${cust.phone}</td><td>${cust.email||'-'}</td><td>${cust.visits||0}</td><td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button></td></tr>`;});h+='</table>';document.getElementById('customerTable').innerHTML=h;}
async function loadAppointments(){const r=await fetch('/api/appointments');const a=await r.json();let h='<table><th>Customer</th><th>Service</th><th>Time</th><th>Status</th><th>Action</th></tr>';a.forEach(app=>{h+=`<tr><td>${app.customer_name}</td><td>${app.service}</td><td>${app.datetime}</td><td><select onchange="updateStatus('${app.id}',this.value)"><option ${app.status==='pending'?'selected':''}>pending</option><option ${app.status==='confirmed'?'selected':''}>confirmed</option><option ${app.status==='completed'?'selected':''}>completed</option></select></td><td><button class="delete-btn" onclick="deleteAppointment('${app.id}')">Cancel</button></td></tr>`;});h+='</table>';document.getElementById('appointmentTable').innerHTML=h;}
async function loadServices(){const r=await fetch('/api/services');const s=await r.json();let h='<table><th>Service</th><th>Price</th><th>Duration</th><th>Category</th><th>Material</th><th>Action</th></tr>';s.forEach(serv=>{h+=`<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.duration}min</td><td>${serv.category}</td><td>$${serv.material_cost||0}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td></tr>`;});h+='</table>';document.getElementById('serviceTable').innerHTML=h;}
async function addService(){await fetch('/api/services',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('newName').value,price:parseInt(document.getElementById('newPrice').value),duration:60,category:document.getElementById('newCat').value,material_cost:parseInt(document.getElementById('newCost').value)||0})});loadServices();}
async function deleteService(id){if(confirm('Delete?')){await fetch('/api/services/'+id,{method:'DELETE'});loadServices();}}
async function deleteCustomer(id){if(confirm('Delete?')){await fetch('/api/customers/'+id,{method:'DELETE'});loadCustomers();loadDashboard();}}
async function deleteAppointment(id){if(confirm('Cancel?')){await fetch('/api/appointments/'+id,{method:'DELETE'});loadAppointments();loadDashboard();}}
async function updateStatus(id,status){await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:status})});loadDashboard();loadAppointments();}
async function askAI(){const q=document.getElementById('aiQuestion').value;if(!q)return;const r=await fetch('/api/ai/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();document.getElementById('aiResponse').innerHTML=d.answer;document.getElementById('aiResponse').style.display='block';}
let lastCount=0;
async function loadNotif(){const r=await fetch('/api/notifications');const n=await r.json();const b=document.getElementById('bellBadge');if(n.length>0){b.style.display='flex';b.innerText=n.length;}else{b.style.display='none';}let h='';n.forEach(not=>{h+=`<div class="notif-item">🔔 ${not.message}<div style="font-size:10px;color:#999;">${not.time}</div></div>`;});document.getElementById('notifList').innerHTML=h||'<div class="notif-item">No notifications</div>';if(n.length>lastCount&&lastCount>0){document.querySelector('.floating-bell').style.transform='scale(1.2)';setTimeout(()=>document.querySelector('.floating-bell').style.transform='scale(1)',300);}lastCount=n.length;}
function toggleNotif(){const p=document.getElementById('notifPopup');p.classList.toggle('show');if(p.classList.contains('show'))loadNotif();}
loadDashboard();loadNotif();setInterval(()=>{if(document.getElementById('dashboard').classList.contains('active'))loadDashboard();loadNotif();},15000);
</script></body></html>
'''

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
    if 'nail' in q: a = "💅 We offer Gel, Acrylic, Polygel, Dip Powder. Prices $15-40. Book now!"
    elif 'lash' in q: a = "👁️ Classic, Volume, Mega Volume lashes. Full sets $35-45, refills $25."
    elif 'skin' in q or 'facial' in q or 'meso' in q: a = "💆 Facials $35-65, Mesotherapy $35-100, HIFU $100. Ask for consultation!"
    elif 'wax' in q: a = "🕯️ Full body $45, Full legs $17, Bikini $23. Pain-free wax!"
    elif 'price' in q: a = "💰 Nails: $15-40, Lashes: $35-45, Skincare: $35-200, Wax: $3-45"
    elif 'book' in q: a = "📅 Tap 'Book Now' tab, pick service, date/time. We'll confirm by SMS!"
    elif 'location' in q or 'address' in q: a = "📍 Bakaata - Ain W ZEIN Road. Call 81023625 for directions!"
    else: a = "✨ Medical Touch: Nails, Lashes, Skincare, Waxing. Questions? Ask away!"
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
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/materials', methods=['GET'])
def get_materials():
    data = load_data()
    services = {s['name']: s for s in data['services']}
    appointments = data['appointments']
    total_rev = 0
    total_mat = 0
    for a in appointments:
        if a.get('status') == 'completed':
            s = services.get(a['service'])
            if s:
                total_rev += s['price']
                total_mat += s.get('material_cost', 0)
    return jsonify({'materials': data.get('materials', {}), 'totalRevenue': total_rev, 'totalMaterialCost': total_mat, 'netProfit': total_rev - total_mat})

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
    t_total = w_total = m_total = y_total = 0
    t_cost = w_cost = m_cost = y_cost = 0
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
                        t_total += s['price']; t_cost += s['material_cost']; t_cnt += 1
                    if d.isocalendar()[1] == week and d.year == year:
                        w_total += s['price']; w_cost += s['material_cost']; w_cnt += 1
                    if d.month == month and d.year == year:
                        m_total += s['price']; m_cost += s['material_cost']; m_cnt += 1
                    if d.year == year:
                        y_total += s['price']; y_cost += s['material_cost']; y_cnt += 1
                except: pass
    popular = [{'name': n, 'count': c, 'netProfit': 0} for n, c in sorted(pop.items(), key=lambda x: x[1], reverse=True)[:6]]
    return jsonify({'profit': {'today': t_total, 'week': w_total, 'month': m_total, 'year': y_total, 'todayNet': t_total - t_cost, 'weekNet': w_total - w_cost, 'monthNet': m_total - m_cost, 'yearNet': y_total - y_cost, 'todayCount': t_cnt, 'weekCount': w_cnt, 'monthCount': m_cnt, 'yearCount': y_cnt}, 'stats': [{'title': 'Customers', 'value': len(data['customers'])}, {'title': 'Appointments', 'value': len(apps)}, {'title': 'Pending', 'value': sum(1 for a in apps if a.get('status') == 'pending')}, {'title': 'Completed', 'value': sum(1 for a in apps if a.get('status') == 'completed')}], 'popular': popular, 'recent': apps[-10:] if apps else []})

@app.route('/api/ai/ask', methods=['POST'])
def ask_ai():
    q = request.json.get('question', '').lower()
    data = load_data()
    apps = data['appointments']
    services = {s['name']: {'price': s['price'], 'material_cost': s.get('material_cost', 0)} for s in data['services']}
    total = sum(services.get(a['service'], {}).get('price', 0) for a in apps if a.get('status') == 'completed')
    materials = sum(services.get(a['service'], {}).get('material_cost', 0) for a in apps if a.get('status') == 'completed')
    net = total - materials
    if 'profit' in q: a = f"💰 Total revenue: ${total}, Materials: ${materials}, Net profit: ${net}. Margin: {((net/total)*100) if total>0 else 0:.1f}%"
    elif 'predict' in q: a = f"📈 Next month projection: ${(total/12)*1.15:.2f} revenue if you maintain current pace"
    else: a = f"💡 You have {len(data['customers'])} customers, {len(apps)} appointments, ${net} net profit. Ask about profits or predictions!"
    return jsonify({'answer': a})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✨ MEDICAL TOUCH CRM v2.0 - WORKING! ✨")
    print("="*60)
    print("\n📍 Customer: https://medical-touch.onrender.com")
    print("🔐 Admin: https://medical-touch.onrender.com/admin")
    print("\n🔑 Login: medicaltouch / admin123")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
