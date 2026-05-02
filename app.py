from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'medicaltouch2024'

DATA_FILE = 'salon_data.json'
ADMIN_USER = "medicaltouch"
ADMIN_PASS = "admin123"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'customers': [], 'appointments': [], 'services': [
        {'id': '1', 'name': 'Full Set GEL + Color Gel', 'price': 35, 'category': 'Nails'},
        {'id': '2', 'name': 'Full Set Lashes Classic', 'price': 35, 'category': 'Lashes'},
        {'id': '3', 'name': 'Facial Classic', 'price': 35, 'category': 'Skincare'},
        {'id': '4', 'name': 'Full Body Wax', 'price': 45, 'category': 'Wax'},
    ]}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Customer Website
CUSTOMER_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Medical Touch</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:Arial;background:#faf8f9;}
.header{background:#1a1a2e;color:white;padding:40px;text-align:center;}
.header h1{font-size:42px;}
.address{background:#ff6b9d;display:inline-block;padding:8px 25px;border-radius:50px;margin-top:15px;}
.tabs{display:flex;justify-content:center;gap:10px;background:white;padding:15px;position:sticky;top:0;}
.tab{padding:10px 25px;border:none;border-radius:40px;cursor:pointer;background:none;}
.tab.active{background:#ff6b9d;color:white;}
.container{padding:40px;max-width:1200px;margin:0 auto;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin-top:20px;}
.service-card{background:white;border-radius:16px;padding:20px;cursor:pointer;border:1px solid #eee;}
.service-price{font-size:24px;font-weight:bold;color:#ff6b9d;}
.booking-section{background:#ffe4e8;border-radius:28px;padding:35px;margin-top:20px;}
input,select{width:100%;padding:12px;margin:10px 0;border:2px solid #eee;border-radius:12px;}
.submit-btn{background:#ff6b9d;color:white;border:none;padding:14px;border-radius:40px;width:100%;cursor:pointer;}
footer{background:#1a1a2e;color:white;text-align:center;padding:30px;margin-top:40px;}
.chat-btn{position:fixed;bottom:30px;right:30px;width:60px;height:60px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:30px;}
.chat-window{position:fixed;bottom:110px;right:30px;width:320px;height:400px;background:white;border-radius:20px;display:none;flex-direction:column;box-shadow:0 5px 20px rgba(0,0,0,0.2);}
.chat-window.show{display:flex;}
.chat-header{background:#ff6b9d;color:white;padding:12px;border-radius:20px 20px 0 0;}
.chat-messages{flex:1;overflow-y:auto;padding:15px;}
.bot-msg{background:#f0f0f0;padding:10px;border-radius:15px;margin:5px 0;}
.user-msg{background:#ff6b9d;color:white;padding:10px;border-radius:15px;margin:5px 0;text-align:right;}
.chat-input{display:flex;padding:10px;border-top:1px solid #ddd;}
.chat-input input{flex:1;margin:0;margin-right:10px;}
.chat-input button{background:#ff6b9d;color:white;border:none;padding:10px 15px;border-radius:25px;cursor:pointer;}
</style></head>
<body>
<div class="header"><h1>MEDICAL TOUCH</h1><div class="address">📍 Bakaata - Ain W ZEIN Road | 📞 81023625</div></div>
<div class="tabs"><button class="tab active" onclick="showTab('services')">💅 Services</button><button class="tab" onclick="showTab('book')">📅 Book</button></div>
<div class="container">
<div id="services" class="tab-content"><div class="services-grid" id="servicesGrid"></div></div>
<div id="book" class="tab-content" style="display:none"><div class="booking-section"><h2>Book Appointment</h2>
<form id="bookForm"><input type="text" id="name" placeholder="Full Name" required><input type="tel" id="phone" placeholder="Phone" required><select id="serviceSelect" required><option value="">Select Service</option></select><input type="datetime-local" id="datetime" required><button type="submit" class="submit-btn">Confirm Booking</button></form></div></div>
</div>
<footer><p>Medical Touch | Bakaata - Ain W ZEIN Road | 81023625</p></footer>
<div class="chat-btn" onclick="toggleChat()">💬</div>
<div class="chat-window" id="chatWindow"><div class="chat-header">🤖 AI Assistant</div><div class="chat-messages" id="chatMsgs"><div class="bot-msg">Hello! Ask me about nails, lashes, skincare, or wax!</div></div><div class="chat-input"><input type="text" id="chatInput" placeholder="Ask me..."><button onclick="sendChat()">Send</button></div></div>
<script>
let services = [];
fetch('/api/services').then(r=>r.json()).then(s=>{services=s;displayServices(s);let opts='<option value="">Select</option>';s.forEach(ss=>{opts+=`<option value="${ss.name}">${ss.name} - $${ss.price}</option>`});document.getElementById('serviceSelect').innerHTML=opts;});
function displayServices(s){let html='';s.forEach(ss=>{html+=`<div class="service-card" onclick="selectService('${ss.name}')"><div class="service-price">$${ss.price}</div><div>${ss.name}</div><div style="color:#ff6b9d;margin-top:10px;">Click to book →</div></div>`;});document.getElementById('servicesGrid').innerHTML=html;}
function selectService(name){document.getElementById('serviceSelect').value=name;showTab('book');}
function showTab(tab){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');document.getElementById('services').style.display=tab==='services'?'block':'none';document.getElementById('book').style.display=tab==='book'?'block':'none';}
document.getElementById('bookForm').onsubmit=async(e)=>{e.preventDefault();const res=await fetch('/api/book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('name').value,phone:document.getElementById('phone').value,service:document.getElementById('serviceSelect').value,datetime:document.getElementById('datetime').value})});const d=await res.json();if(d.success)alert('✅ Booked!');else alert('❌ Time taken or error');};
function toggleChat(){document.getElementById('chatWindow').classList.toggle('show');}
async function sendChat(){const q=document.getElementById('chatInput').value;if(!q)return;const msgs=document.getElementById('chatMsgs');msgs.innerHTML+=`<div class="user-msg">${q}</div>`;document.getElementById('chatInput').value='';const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const d=await r.json();msgs.innerHTML+=`<div class="bot-msg">${d.answer}</div>`;msgs.scrollTop=msgs.scrollHeight;}
</script>
</body></html>
'''

# Admin Dashboard
ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Medical Touch Admin</title><style>
*{margin:0;padding:0;box-sizing:border-box;}body{font-family:Arial;background:#f0f2f5;}
.sidebar{width:250px;background:#1a1a2e;color:white;position:fixed;height:100%;padding:20px;}
.sidebar a{display:block;color:white;padding:12px;margin:5px 0;text-decoration:none;border-radius:8px;cursor:pointer;}
.sidebar a:hover{background:#ff6b9d;}
.main{margin-left:250px;padding:20px;}
.top-bar{background:white;padding:15px;border-radius:12px;margin-bottom:20px;display:flex;justify-content:space-between;}
.section{background:white;border-radius:16px;padding:20px;margin-bottom:20px;display:none;}
.section.active{display:block;}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:20px;}
.stat-card{background:white;padding:20px;border-radius:12px;text-align:center;}
.stat-number{font-size:32px;font-weight:bold;color:#ff6b9d;}
table{width:100%;border-collapse:collapse;}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;}
.delete-btn{background:#dc3545;color:white;border:none;padding:5px 10px;border-radius:5px;cursor:pointer;}
input,select{padding:8px;margin:5px;border:1px solid #ddd;border-radius:6px;}
button{background:#ff6b9d;color:white;border:none;padding:8px 15px;border-radius:6px;cursor:pointer;}
.logout-btn{background:#ff4d7d;padding:8px 20px;border-radius:20px;border:none;cursor:pointer;color:white;}
.bell{position:fixed;bottom:30px;right:30px;width:55px;height:55px;background:#ff6b9d;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:25px;}
.notif-popup{position:fixed;bottom:100px;right:30px;width:300px;background:white;border-radius:12px;display:none;box-shadow:0 5px 15px rgba(0,0,0,0.2);}
.notif-popup.show{display:block;}
.notif-header{background:#ff6b9d;color:white;padding:10px;border-radius:12px 12px 0 0;}
.notif-item{padding:10px;border-bottom:1px solid #eee;}
</style></head>
<body>
<div class="sidebar"><h2>Medical Touch</h2><a onclick="showSection('dashboard')">📊 Dashboard</a><a onclick="showSection('customers')">👥 Customers</a><a onclick="showSection('appointments')">📅 Appointments</a><a onclick="showSection('services')">💅 Services</a></div>
<div class="main"><div class="top-bar"><h2>Admin Panel</h2><button class="logout-btn" onclick="location.href='/logout'">Logout</button></div>
<div id="dashboard" class="section active"><div class="stats" id="stats"></div><h3>Recent Bookings</h3><div id="recent"></div></div>
<div id="customers" class="section"><h2>Customers</h2><div id="customerTable"></div></div>
<div id="appointments" class="section"><h2>Appointments</h2><div id="appointmentTable"></div></div>
<div id="services" class="section"><h2>Services</h2><div><input type="text" id="newName" placeholder="Name"><input type="number" id="newPrice" placeholder="Price"><select id="newCat"><option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option></select><button onclick="addService()">Add</button></div><div id="serviceTable"></div></div></div>
<div class="bell" onclick="toggleNotif()">🔔<span id="bellBadge" style="position:absolute;top:-5px;right:-5px;background:red;border-radius:50%;width:18px;height:18px;font-size:10px;display:none;"></span></div>
<div id="notifPopup" class="notif-popup"><div class="notif-header">Notifications</div><div id="notifList"></div></div>
<script>
let profitData={};
function showSection(s){document.querySelectorAll('.section').forEach(sec=>sec.classList.remove('active'));document.getElementById(s).classList.add('active');if(s==='dashboard')loadDashboard();if(s==='customers')loadCustomers();if(s==='appointments')loadAppointments();if(s==='services')loadServices();}
async function loadDashboard(){const r=await fetch('/api/stats');const d=await r.json();document.getElementById('stats').innerHTML=d.stats.map(s=>`<div class="stat-card"><div class="stat-number">${s.value}</div><div>${s.title}</div></div>`).join('');document.getElementById('recent').innerHTML=d.recent.map(a=>`<div style="padding:10px;border-left:3px solid #ff6b9d;margin:5px 0;"><strong>${a.customer_name}</strong> - ${a.service}<br>${a.datetime}</div>`).join('')||'<p>No appointments</p>';}
async function loadCustomers(){const r=await fetch('/api/customers');const c=await r.json();document.getElementById('customerTable').innerHTML='<table><tr><th>Name</th><th>Phone</th><th>Email</th><th>Action</th></tr>'+c.map(cust=>`<tr><td>${cust.name}</td><td>${cust.phone}</td><td>${cust.email||'-'}</td><td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button></td></tr>`).join('')+'</table>';}
async function loadAppointments(){const r=await fetch('/api/appointments');const a=await r.json();document.getElementById('appointmentTable').innerHTML='<table><tr><th>Customer</th><th>Service</th><th>Time</th><th>Status</th><th>Action</th></tr>'+a.map(app=>`<tr><td>${app.customer_name}</td><td>${app.service}</td><td>${app.datetime}</td><td><select onchange="updateStatus('${app.id}',this.value)"><option ${app.status==='pending'?'selected':''}>pending</option><option ${app.status==='confirmed'?'selected':''}>confirmed</option><option ${app.status==='completed'?'selected':''}>completed</option></select></td><td><button class="delete-btn" onclick="deleteAppointment('${app.id}')">Cancel</button></td></tr>`).join('')+'</table>';}
async function loadServices(){const r=await fetch('/api/services');const s=await r.json();document.getElementById('serviceTable').innerHTML='<table><tr><th>Name</th><th>Price</th><th>Category</th><th>Action</th></tr>'+s.map(serv=>`<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.category}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td></tr>`).join('')+'</table>';}
async function addService(){await fetch('/api/services',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('newName').value,price:parseInt(document.getElementById('newPrice').value),category:document.getElementById('newCat').value})});loadServices();}
async function deleteService(id){if(confirm('Delete?')){await fetch('/api/services/'+id,{method:'DELETE'});loadServices();}}
async function deleteCustomer(id){if(confirm('Delete?')){await fetch('/api/customers/'+id,{method:'DELETE'});loadCustomers();loadDashboard();}}
async function deleteAppointment(id){if(confirm('Cancel?')){await fetch('/api/appointments/'+id,{method:'DELETE'});loadAppointments();loadDashboard();}}
async function updateStatus(id,status){await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status})});loadDashboard();loadAppointments();}
async function loadNotif(){const r=await fetch('/api/notifications');const n=await r.json();const b=document.getElementById('bellBadge');if(n.length>0){b.style.display='flex';b.innerText=n.length;}else{b.style.display='none';}document.getElementById('notifList').innerHTML=n.map(not=>`<div class="notif-item">🔔 ${not.message}<div style="font-size:10px;color:#999;">${not.time}</div></div>`).join('')||'<div>No notifications</div>';}
function toggleNotif(){document.getElementById('notifPopup').classList.toggle('show');if(document.getElementById('notifPopup').classList.contains('show'))loadNotif();}
loadDashboard();loadNotif();setInterval(()=>{if(document.getElementById('dashboard').classList.contains('active'))loadDashboard();loadNotif();},15000);
</script></body></html>
'''

@app.route('/')
def home():
    return render_template_string(CUSTOMER_HTML)

@app.route('/admin')
def admin_login_page():
    return render_template_string(LOGIN_PAGE)

LOGIN_PAGE = '''
<!DOCTYPE html>
<html><body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a2e;"><div style="background:white;padding:40px;border-radius:20px;"><h2>Admin Login</h2>
<form method="POST"><input type="text" name="username" placeholder="Username" style="width:100%;padding:10px;margin:10px 0;"><input type="password" name="password" placeholder="Password" style="width:100%;padding:10px;margin:10px 0;"><button type="submit" style="background:#ff6b9d;color:white;padding:10px 20px;border:none;border-radius:10px;">Login</button></form>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}</div></body></html>
'''

@app.route('/admin', methods=['POST'])
def admin_login():
    if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template_string(LOGIN_PAGE, error='Wrong credentials')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login_page'))
    return render_template_string(ADMIN_HTML)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(load_data()['services'])

@app.route('/api/services', methods=['POST'])
def add_service():
    d = load_data()
    new = request.json
    new['id'] = str(len(d['services']) + 1)
    new['duration'] = 60
    d['services'].append(new)
    save_data(d)
    return jsonify({'success': True})

@app.route('/api/services/<sid>', methods=['DELETE'])
def del_service(sid):
    d = load_data()
    d['services'] = [s for s in d['services'] if s['id'] != sid]
    save_data(d)
    return jsonify({'success': True})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(load_data()['customers'])

@app.route('/api/customers/<cid>', methods=['DELETE'])
def del_customer(cid):
    d = load_data()
    d['customers'] = [c for c in d['customers'] if c['id'] != cid]
    d['appointments'] = [a for a in d['appointments'] if a['customer_id'] != cid]
    save_data(d)
    return jsonify({'success': True})

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    return jsonify(load_data()['appointments'])

@app.route('/api/appointments/<aid>', methods=['DELETE'])
def del_appointment(aid):
    d = load_data()
    d['appointments'] = [a for a in d['appointments'] if a['id'] != aid]
    save_data(d)
    return jsonify({'success': True})

@app.route('/api/appointments/<aid>/status', methods=['PUT'])
def upd_status(aid):
    d = load_data()
    for a in d['appointments']:
        if a['id'] == aid:
            a['status'] = request.json.get('status')
            break
    save_data(d)
    return jsonify({'success': True})

@app.route('/api/book', methods=['POST'])
def book():
    d = load_data()
    b = request.json
    for a in d['appointments']:
        if a['datetime'] == b['datetime']:
            return jsonify({'success': False, 'error': 'time taken'})
    cust = next((c for c in d['customers'] if c['phone'] == b['phone']), None)
    if not cust:
        cust = {'id': str(len(d['customers']) + 1), 'name': b['name'], 'phone': b['phone'], 'email': '', 'visits': 0}
        d['customers'].append(cust)
    appt = {'id': str(len(d['appointments']) + 1), 'customer_id': cust['id'], 'customer_name': cust['name'], 'service': b['service'], 'datetime': b['datetime'], 'status': 'pending'}
    d['appointments'].append(appt)
    save_data(d)
    return jsonify({'success': True})

@app.route('/api/chat', methods=['POST'])
def chat():
    q = request.json.get('question', '').lower()
    if 'nail' in q: a = "💅 Nail services: Gel $35, Acrylic $40, Manicure $10"
    elif 'lash' in q: a = "👁️ Lashes: Classic $35, Volume $38, Mega $45"
    elif 'skin' in q: a = "💆 Facials $35-65, Mesotherapy $35-100"
    elif 'wax' in q: a = "🕯️ Wax: Full body $45, Bikini $23, Legs $17"
    elif 'book' in q: a = "📅 Go to Book tab, select service and time!"
    else: a = "✨ Medical Touch: Nails, Lashes, Skincare, Wax. Ask anything!"
    return jsonify({'answer': a})

@app.route('/api/stats', methods=['GET'])
def stats():
    d = load_data()
    apps = d['appointments']
    return jsonify({
        'stats': [
            {'title': 'Customers', 'value': len(d['customers'])},
            {'title': 'Appointments', 'value': len(apps)},
            {'title': 'Pending', 'value': sum(1 for a in apps if a.get('status') == 'pending')},
            {'title': 'Completed', 'value': sum(1 for a in apps if a.get('status') == 'completed')}
        ],
        'recent': apps[-5:] if apps else []
    })

@app.route('/api/notifications', methods=['GET'])
def get_notifs():
    return jsonify([])

if __name__ == '__main__':
    print("\n" + "="*50)
    print("MEDICAL TOUCH CRM - WORKING!")
    print("="*50)
    print("\nCustomer: https://medical-touch.onrender.com")
    print("Admin: https://medical-touch.onrender.com/admin")
    print("\nLogin: medicaltouch / admin123")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
