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

# ADMIN CREDENTIALS - CHANGE THESE!
ADMIN_USERNAME = "medicaltouch"
ADMIN_PASSWORD = "admin123"

# Login required decorator
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
            {'id': '1', 'name': 'Full Set GEL + Manicure', 'price': 40, 'duration': 90, 'category': 'Nails', 'material_cost': 5},
            {'id': '2', 'name': 'Full Set Fiber GEL', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 4},
            {'id': '3', 'name': 'Full Set Polygel', 'price': 35, 'duration': 75, 'category': 'Nails', 'material_cost': 4},
            {'id': '4', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '5', 'name': 'Full Set Lashes Volume', 'price': 38, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '6', 'name': 'Facial Classic', 'price': 35, 'duration': 60, 'category': 'Skincare', 'material_cost': 3},
            {'id': '7', 'name': 'Hydra Facial', 'price': 55, 'duration': 75, 'category': 'Skincare', 'material_cost': 8},
            {'id': '8', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax', 'material_cost': 3},
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
        'time': datetime.now().strftime('%I:%M %p %Y-%m-%d'),
        'read': False
    })
    save_notifications(notifs[:50])

def check_double_booking(staff_id, datetime_str):
    data = load_data()
    for a in data['appointments']:
        if a.get('staff_id') == staff_id and a.get('datetime') == datetime_str and a.get('status') != 'cancelled':
            return True
    return False

# Format time helper
def format_time(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%I:%M %p').lstrip('0')
    except:
        return dt_str

# Admin Login Page HTML
LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login - Medical Touch</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); min-height: 100vh; display: flex; justify-content: center; align-items: center; }
        .login-box { background: white; padding: 40px; border-radius: 20px; width: 380px; text-align: center; }
        .logo { font-size: 50px; margin-bottom: 20px; }
        h2 { color: #ff6b9d; margin-bottom: 10px; }
        .sub { color: #666; font-size: 14px; margin-bottom: 30px; }
        input { width: 100%; padding: 14px; margin: 10px 0; border: 2px solid #eee; border-radius: 12px; font-size: 16px; }
        input:focus { outline: none; border-color: #ff6b9d; }
        button { background: #ff6b9d; color: white; border: none; padding: 14px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; }
        button:hover { background: #ff4d7d; }
        .error { color: red; margin-top: 15px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">🔐</div>
        <h2>Medical Touch Admin</h2>
        <div class="sub">Enter your credentials</div>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

# Customer AI Booking HTML
CUSTOMER_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Medical Touch | Beauty & Wellness</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #faf8f9; }
        .header { background: #1a1a2e; color: white; padding: 40px 20px; text-align: center; }
        .logo-circle { width: 70px; height: 70px; background: #ff6b9d; border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 35px; }
        .header h1 { font-family: 'Playfair Display', serif; font-size: 42px; }
        .phone { margin-top: 12px; font-size: 18px; }
        .tabs { display: flex; justify-content: center; gap: 5px; background: white; padding: 10px; position: sticky; top: 0; flex-wrap: wrap; }
        .tab { padding: 10px 25px; font-size: 15px; background: none; border: none; cursor: pointer; border-radius: 30px; color: #666; }
        .tab.active { background: #ff6b9d; color: white; }
        .container { max-width: 1200px; margin: 0 auto; padding: 30px 20px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .services-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
        .service-card { background: white; border-radius: 16px; padding: 20px; cursor: pointer; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #eee; }
        .service-card:hover { transform: translateY(-2px); border-color: #ff6b9d; }
        .service-name { font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }
        .service-price { font-size: 24px; font-weight: bold; color: #ff6b9d; }
        .booking-section { background: linear-gradient(135deg, #fff5f7, #ffe4e8); border-radius: 24px; padding: 35px; }
        input, select { width: 100%; padding: 12px; border: 2px solid #eee; border-radius: 12px; margin: 10px 0; }
        .submit-btn { background: #ff6b9d; color: white; padding: 12px; border: none; border-radius: 30px; width: 100%; cursor: pointer; font-weight: bold; }
        footer { background: #1a1a2e; color: white; text-align: center; padding: 30px; }
    </style>
</head>
<body>
    <div class="header"><div class="logo-circle">💅</div><h1>MEDICAL TOUCH</h1><div class="phone">📞 81023625</div></div>
    <div class="tabs">
        <button class="tab active" onclick="switchTab('nails')">Nails</button>
        <button class="tab" onclick="switchTab('lashes')">Lashes</button>
        <button class="tab" onclick="switchTab('skincare')">Skincare</button>
        <button class="tab" onclick="switchTab('wax')">Wax</button>
        <button class="tab" onclick="switchTab('book')">Book</button>
    </div>
    <div class="container">
        <div id="nails" class="tab-content active"><div class="services-grid" id="nailsGrid"></div></div>
        <div id="lashes" class="tab-content"><div class="services-grid" id="lashesGrid"></div></div>
        <div id="skincare" class="tab-content"><div class="services-grid" id="skincareGrid"></div></div>
        <div id="wax" class="tab-content"><div class="services-grid" id="waxGrid"></div></div>
        <div id="book" class="tab-content">
            <div class="booking-section">
                <h2>Book Your Appointment</h2>
                <form id="bookingForm">
                    <input type="text" id="custName" placeholder="Full Name" required>
                    <input type="tel" id="custPhone" placeholder="Phone Number" required>
                    <input type="email" id="custEmail" placeholder="Email">
                    <select id="serviceSelect" required><option value="">Select Service</option></select>
                    <input type="datetime-local" id="appointmentDate" required>
                    <div id="slotWarning" style="color:red; font-size:12px; display:none;">⚠️ This time slot is already booked! Please choose another time.</div>
                    <button type="submit" class="submit-btn">Confirm Booking</button>
                </form>
            </div>
        </div>
    </div>
    <footer><p>Medical Touch | Where Beauty Meets Medical Excellence | 81023625</p></footer>
    <script>
        let allServices = [];
        let bookedSlots = [];
        
        fetch('/api/services').then(r=>r.json()).then(services=> {
            allServices = services;
            displayServices(services);
            populateSelect(services);
        });
        
        fetch('/api/booked-slots').then(r=>r.json()).then(slots=> { bookedSlots = slots; });
        
        function displayServices(services) {
            const cats = {Nails:'nailsGrid',Lashes:'lashesGrid',Skincare:'skincareGrid',Wax:'waxGrid'};
            for(let [cat, elId] of Object.entries(cats)) {
                let filtered = services.filter(s => s.category === cat);
                let html = '';
                filtered.forEach(s => { html += `<div class="service-card" onclick="bookService('${s.name}')"><div class="service-name">${s.name}</div><div class="service-price">$${s.price}</div><div style="font-size:12px;color:#999;">${s.duration} min</div><div style="margin-top:10px;color:#ff6b9d;">Click to book →</div></div>`; });
                document.getElementById(elId).innerHTML = html || '<p>Loading...</p>';
            }
        }
        
        function populateSelect(services) {
            let html = '<option value="">Select service</option>';
            services.forEach(s => { html += `<option value="${s.name}">${s.name} - $${s.price}</option>`; });
            document.getElementById('serviceSelect').innerHTML = html;
        }
        
        function bookService(name) {
            document.getElementById('serviceSelect').value = name;
            switchTab('book');
        }
        
        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById(tab).classList.add('active');
        }
        
        document.getElementById('appointmentDate').onchange = function() {
            fetch('/api/check-slot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({datetime: this.value})
            }).then(r=>r.json()).then(data => {
                document.getElementById('slotWarning').style.display = data.booked ? 'block' : 'none';
            });
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
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            if(result.success) alert('Appointment booked! Check SMS for confirmation.');
            else if(result.double_booking) alert('Sorry, this time is already taken. Please choose another time.');
            else alert('Error. Please try again.');
            if(result.success) document.getElementById('bookingForm').reset();
        };
    </script>
</body>
</html>
'''

# Admin Dashboard HTML with Most Wanted Wheel
ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Medical Touch | Admin</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #f0f2f5; }
        .sidebar { width: 260px; background: #1a1a2e; color: white; position: fixed; height: 100%; padding: 25px; }
        .sidebar h2 { font-size: 20px; margin-bottom: 30px; }
        .sidebar nav a { display: block; color: white; text-decoration: none; padding: 10px 15px; margin: 5px 0; border-radius: 10px; }
        .sidebar nav a:hover { background: #ff6b9d; }
        .main { margin-left: 260px; padding: 25px; }
        .top-bar { background: white; padding: 15px 25px; border-radius: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 25px; }
        .stat-card { background: white; border-radius: 15px; padding: 20px; text-align: center; }
        .stat-card .number { font-size: 32px; font-weight: bold; color: #ff6b9d; }
        
        .wheels-container { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }
        .wheel-card { background: white; border-radius: 20px; padding: 25px; text-align: center; }
        .wheel { display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin: 20px 0; }
        .wheel-item { width: 100px; height: 100px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; cursor: pointer; }
        .section { background: white; border-radius: 20px; padding: 25px; margin-bottom: 25px; display: none; }
        .section.active { display: block; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #fef8f9; color: #ff6b9d; }
        .delete-btn, .edit-btn { background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; }
        .edit-btn { background: #ffc107; color: #333; }
        input, select { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 8px; }
        button { background: #ff6b9d; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; }
        .profit-detail { margin-top: 15px; padding: 15px; background: #fef8f9; border-radius: 12px; display: none; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>💅 Medical Touch</h2>
        <nav>
            <a href="#" onclick="showSection('dashboard')">📊 Dashboard</a>
            <a href="#" onclick="showSection('materials')">📦 Materials</a>
            <a href="#" onclick="showSection('customers')">👥 Customers</a>
            <a href="#" onclick="showSection('appointments')">📅 Appointments</a>
            <a href="#" onclick="showSection('services')">💅 Services</a>
            <a href="#" onclick="showSection('ai')">🤖 AI</a>
        </nav>
    </div>
    <div class="main">
        <div class="top-bar"><h2>Admin Dashboard</h2><div style="display:flex; gap:15px;"><button onclick="location.href='/admin/logout'">Logout</button></div></div>
        
        <div id="dashboard" class="section active">
            <div class="wheels-container">
                <div class="wheel-card"><h3>💰 Profit Wheels</h3><div class="wheel">
                    <div class="wheel-item" style="background:#1a1a2e;" onclick="showProfit('today')"><span id="todayAmt">$0</span><div>Today</div></div>
                    <div class="wheel-item" style="background:#ff6b9d;" onclick="showProfit('week')"><span id="weekAmt">$0</span><div>Week</div></div>
                    <div class="wheel-item" style="background:#ff4d7d;" onclick="showProfit('month')"><span id="monthAmt">$0</span><div>Month</div></div>
                    <div class="wheel-item" style="background:#1a1a2e;" onclick="showProfit('year')"><span id="yearAmt">$0</span><div>Year</div></div>
                </div><div id="profitDetail" class="profit-detail"></div></div>
                
                <div class="wheel-card"><h3>🎯 Most Wanted Services</h3><div class="wheel" id="popularWheel"></div><div id="popularDetail" class="profit-detail"></div></div>
            </div>
            <div class="stats-grid" id="statsGrid"></div>
            <h3>Recent Bookings</h3><div id="recentList"></div>
        </div>
        
        <div id="materials" class="section"><h2>📦 Materials & Costs</h2><div id="materialsGrid"></div><div id="profitSummary" style="margin-top:20px;padding:20px;background:#fef8f9;border-radius:15px;"></div></div>
        <div id="customers" class="section"><h2>👥 Customers</h2><div id="customerTable"></div></div>
        <div id="appointments" class="section"><h2>📅 Appointments</h2><div id="appointmentTable"></div></div>
        <div id="services" class="section"><h2>💅 Services</h2><div><input type="text" id="newName" placeholder="Name"><input type="number" id="newPrice" placeholder="Price"><select id="newCat"><option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option></select><input type="number" id="newCost" placeholder="Material Cost"><button onclick="addService()">Add</button></div><div id="serviceTable" style="margin-top:15px"></div></div>
        <div id="ai" class="section"><div class="ai-box"><h2>🤖 AI Assistant</h2><p>Ask about profits, predictions, or materials</p><div><input type="text" id="aiQuestion" placeholder="How much profit after materials?" style="width:70%"><button onclick="askAI()">Ask</button></div><div id="aiResponse" style="margin-top:15px;padding:15px;background:#fef8f9;border-radius:12px;display:none;"></div></div></div>
    </div>
    <script>
        let profitData = {};
        let popularData = {};
        
        function showSection(s) {
            document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
            document.getElementById(s).classList.add('active');
            if(s === 'dashboard') loadDashboard();
            if(s === 'materials') loadMaterials();
            if(s === 'customers') loadCustomers();
            if(s === 'appointments') loadAppointments();
            if(s === 'services') loadServices();
        }
        
        async function loadDashboard() {
            const r = await fetch('/api/admin/stats');
            const d = await r.json();
            profitData = d.profit;
            popularData = d.popular;
            document.getElementById('todayAmt').innerText = '$'+profitData.today;
            document.getElementById('weekAmt').innerText = '$'+profitData.week;
            document.getElementById('monthAmt').innerText = '$'+profitData.month;
            document.getElementById('yearAmt').innerText = '$'+profitData.year;
            let statsHtml = '';
            d.stats.forEach(s => { statsHtml += `<div class="stat-card"><h3>${s.title}</h3><div class="number">${s.value}</div></div>`; });
            document.getElementById('statsGrid').innerHTML = statsHtml;
            let popularHtml = '';
            const colors = ['#ff6b9d', '#ff4d7d', '#ffb347', '#4ecdc4', '#45b7d1', '#96ceb4'];
            popularData.forEach((p,i) => { popularHtml += `<div class="wheel-item" style="background:${colors[i%colors.length]}" onclick="showPopular('${p.name}')"><span>${p.name}</span><div>${p.count} bookings</div></div>`; });
            document.getElementById('popularWheel').innerHTML = popularHtml || '<p>No data yet</p>';
            let recentHtml = '';
            d.recent.forEach(a => { recentHtml += `<div style="padding:10px;margin:5px 0;border-left:3px solid #ff6b9d;background:#f8f9fa;"><strong>${a.customer_name}</strong> - ${a.service}<br>${a.datetime} | ${a.status}</div>`; });
            document.getElementById('recentList').innerHTML = recentHtml || '<p>No appointments</p>';
        }
        
        function showProfit(p) {
            const d = document.getElementById('profitDetail');
            let msg = '';
            if(p === 'today') msg = `💰 Today: $${profitData.today} (${profitData.todayCount||0} appts) | Net Profit: $${profitData.todayNet||0}`;
            if(p === 'week') msg = `💰 Week: $${profitData.week} (${profitData.weekCount||0} appts) | Net Profit: $${profitData.weekNet||0}`;
            if(p === 'month') msg = `💰 Month: $${profitData.month} (${profitData.monthCount||0} appts) | Net Profit: $${profitData.monthNet||0}`;
            if(p === 'year') msg = `💰 Year: $${profitData.year} (${profitData.yearCount||0} appts) | Net Profit: $${profitData.yearNet||0}`;
            d.innerHTML = msg;
            d.style.display = 'block';
            setTimeout(() => d.style.display = 'none', 4000);
        }
        
        function showPopular(name) {
            const d = document.getElementById('popularDetail');
            const p = popularData.find(x => x.name === name);
            if(p) d.innerHTML = `🎯 ${p.name}: ${p.count} bookings | Revenue: $${p.revenue} | Est. Material Cost: $${p.materialCost} | Net: $${p.netProfit}`;
            else d.innerHTML = 'No data';
            d.style.display = 'block';
            setTimeout(() => d.style.display = 'none', 4000);
        }
        
        async function loadMaterials() {
            const r = await fetch('/api/materials');
            const d = await r.json();
            let html = '<table><tr><th>Category</th><th>Monthly Material Cost</th><th>Items</th><th>Action</th></tr>';
            for(let cat in d.materials) {
                html += `<tr><td>${cat}</td><td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:100px"></td><td>${d.materials[cat].items.join(', ')}</td><td><button onclick="updateMaterialCost('${cat}')">Update</button></td></tr>`;
            }
            html += '</table>';
            document.getElementById('materialsGrid').innerHTML = html;
            document.getElementById('profitSummary').innerHTML = `<h3>💰 Profit Summary</h3><p>Total Revenue: $${d.totalRevenue} | Total Material Cost: $${d.totalMaterialCost} | Net Profit: $${d.netProfit}</p>`;
        }
        
        async function updateMaterialCost(cat) {
            const cost = document.getElementById(`cost_${cat}`).value;
            await fetch('/api/materials/update', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat, cost:parseInt(cost)})});
            loadMaterials();
        }
        
        async function loadCustomers() {
            const r = await fetch('/api/customers'); const c = await r.json();
            let h = '<table><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Action</th></tr>';
            c.forEach(cust => { h += `<tr><td>${cust.name}</td><td>${cust.phone}</td><td>${cust.email||'-'}</td><td>${cust.visits||0}</td><td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button></td>`; });
            h += '</table>'; document.getElementById('customerTable').innerHTML = h;
        }
        
        async function loadAppointments() {
            const r = await fetch('/api/appointments'); const a = await r.json();
            let h = '<table><th>Customer</th><th>Service</th><th>Date & Time</th><th>Status</th><th>Action</th></tr>';
            a.forEach(app => { h += `<tr><td>${app.customer_name}</td><td>${app.service}</td><td>${app.datetime}</td><td><select onchange="updateStatus('${app.id}',this.value)"><option ${app.status==='pending'?'selected':''}>pending</option><option ${app.status==='confirmed'?'selected':''}>confirmed</option><option ${app.status==='completed'?'selected':''}>completed</option></select></td><td><button class="delete-btn" onclick="deleteAppointment('${app.id}')">Cancel</button></td>`; });
            h += '</table>'; document.getElementById('appointmentTable').innerHTML = h;
        }
        
        async function loadServices() {
            const r = await fetch('/api/services'); const s = await r.json();
            let h = '<table><th>Service</th><th>Price</th><th>Duration</th><th>Category</th><th>Material Cost</th><th>Action</th></tr>';
            s.forEach(serv => { h += `<tr><td>${serv.name}</td><td>$${serv.price}</td><td>${serv.duration} min</td><td>${serv.category}</td><td>$${serv.material_cost||0}</td><td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td>`; });
            h += '</table>'; document.getElementById('serviceTable').innerHTML = h;
        }
        
        async function addService() {
            await fetch('/api/services', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
                name:document.getElementById('newName').value,
                price:parseInt(document.getElementById('newPrice').value),
                duration:60,
                category:document.getElementById('newCat').value,
                material_cost:parseInt(document.getElementById('newCost').value)||0
            })});
            loadServices();
        }
        
        async function deleteService(id) { if(confirm('Delete?')) { await fetch('/api/services/'+id,{method:'DELETE'}); loadServices(); } }
        async function deleteCustomer(id) { if(confirm('Delete?')) { await fetch('/api/customers/'+id,{method:'DELETE'}); loadCustomers(); loadDashboard(); } }
        async function deleteAppointment(id) { if(confirm('Cancel?')) { await fetch('/api/appointments/'+id,{method:'DELETE'}); loadAppointments(); loadDashboard(); } }
        async function updateStatus(id, status) { await fetch('/api/appointments/'+id+'/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:status})}); loadDashboard(); loadAppointments(); }
        
        async function askAI() {
            const q = document.getElementById('aiQuestion').value;
            if(!q) return;
            const r = await fetch('/api/ai/ask', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
            const d = await r.json();
            document.getElementById('aiResponse').innerHTML = d.answer;
            document.getElementById('aiResponse').style.display = 'block';
        }
        
        loadDashboard();
        setInterval(() => { if(document.getElementById('dashboard').classList.contains('active')) loadDashboard(); }, 30000);
    </script>
</body>
</html>
'''

# API Routes
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

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(load_data()['services'])

@app.route('/api/services', methods=['POST'])
def add_service():
    data = load_data()
    new_service = request.json
    new_service['id'] = str(len(data['services']) + 1)
    data['services'].append(new_service)
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    data = load_data()
    data['services'] = [s for s in data['services'] if s['id'] != service_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/booked-slots', methods=['GET'])
def get_booked_slots():
    data = load_data()
    slots = [{'datetime': a['datetime'], 'staff_id': a.get('staff_id', 'staff1')} for a in data['appointments'] if a.get('status') != 'cancelled']
    return jsonify(slots)

@app.route('/api/check-slot', methods=['POST'])
def check_slot():
    data = request.json
    booked = check_double_booking('staff1', data['datetime'])
    return jsonify({'booked': booked})

@app.route('/api/customer-book', methods=['POST'])
def customer_book():
    data = load_data()
    booking = request.json
    
    if check_double_booking('staff1', booking['datetime']):
        return jsonify({'success': False, 'double_booking': True})
    
    customer = next((c for c in data['customers'] if c['phone'] == booking['phone']), None)
    if not customer:
        customer = {'id': str(len(data['customers']) + 1), 'name': booking['name'], 'phone': booking['phone'], 'email': booking.get('email', ''), 'visits': 0}
        data['customers'].append(customer)
    
    appointment = {'id': str(len(data['appointments']) + 1), 'customer_id': customer['id'], 'customer_name': customer['name'], 'service': booking['service'], 'datetime': booking['datetime'], 'status': 'pending', 'staff_id': 'staff1', 'booked_at': datetime.now().isoformat()}
    data['appointments'].append(appointment)
    save_data(data)
    add_notification(f"New booking: {customer['name']} - {booking['service']} at {booking['datetime']}")
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
                customer = next((c for c in data['customers'] if c['id'] == a['customer_id']), None)
                if customer:
                    customer['visits'] = customer.get('visits', 0) + 1
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/materials', methods=['GET'])
def get_materials():
    data = load_data()
    services = data['services']
    appointments = data['appointments']
    materials = data.get('materials', {})
    
    total_revenue = 0
    total_material_cost = 0
    
    for a in appointments:
        if a.get('status') == 'completed':
            service = next((s for s in services if s['name'] == a['service']), None)
            if service:
                total_revenue += service['price']
                total_material_cost += service.get('material_cost', 0)
    
    return jsonify({
        'materials': materials,
        'totalRevenue': total_revenue,
        'totalMaterialCost': total_material_cost,
        'netProfit': total_revenue - total_material_cost
    })

@app.route('/api/materials/update', methods=['POST'])
def update_materials():
    data = load_data()
    req = request.json
    data['materials'][req['category']]['cost'] = req['cost']
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/admin/stats', methods=['GET'])
@login_required
def admin_stats():
    data = load_data()
    appointments = data['appointments']
    services_data = {s['name']: {'price': s['price'], 'material_cost': s.get('material_cost', 0), 'category': s['category']} for s in data['services']}
    
    today = datetime.now().strftime('%Y-%m-%d')
    current_week = datetime.now().isocalendar()[1]
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Stats
    total_customers = len(data['customers'])
    total_appointments = len(appointments)
    pending = sum(1 for a in appointments if a.get('status') == 'pending')
    completed = sum(1 for a in appointments if a.get('status') == 'completed')
    
    # Profit calculations
    today_total = week_total = month_total = year_total = 0
    today_cost = week_cost = month_cost = year_cost = 0
    today_count = week_count = month_count = year_count = 0
    
    # Popular services
    service_counts = {}
    service_revenue = {}
    service_material_cost = {}
    
    for a in appointments:
        service = services_data.get(a['service'])
        if not service:
            continue
        
        price = service['price']
        cost = service['material_cost']
        
        # Count for popular
        service_counts[a['service']] = service_counts.get(a['service'], 0) + 1
        service_revenue[a['service']] = service_revenue.get(a['service'], 0) + (price if a.get('status') == 'completed' else 0)
        service_material_cost[a['service']] = service_material_cost.get(a['service'], 0) + (cost if a.get('status') == 'completed' else 0)
        
        if a.get('status') == 'completed':
            try:
                date_obj = datetime.fromisoformat(a['datetime'])
                date_str = date_obj.strftime('%Y-%m-%d')
                week_num = date_obj.isocalendar()[1]
                if date_str == today:
                    today_total += price; today_cost += cost; today_count += 1
                if week_num == current_week and date_obj.year == current_year:
                    week_total += price; week_cost += cost; week_count += 1
                if date_obj.month == current_month and date_obj.year == current_year:
                    month_total += price; month_cost += cost; month_count += 1
                if date_obj.year == current_year:
                    year_total += price; year_cost += cost; year_count += 1
            except:
                pass
    
    popular = []
    for name, count in sorted(service_counts.items(), key=lambda x: x[1], reverse=True)[:6]:
        popular.append({
            'name': name,
            'count': count,
            'revenue': service_revenue.get(name, 0),
            'materialCost': service_material_cost.get(name, 0),
            'netProfit': service_revenue.get(name, 0) - service_material_cost.get(name, 0)
        })
    
    return jsonify({
        'profit': {
            'today': today_total, 'week': week_total, 'month': month_total, 'year': year_total,
            'todayCount': today_count, 'weekCount': week_count, 'monthCount': month_count, 'yearCount': year_count,
            'todayNet': today_total - today_cost, 'weekNet': week_total - week_cost,
            'monthNet': month_total - month_cost, 'yearNet': year_total - year_cost
        },
        'stats': [
            {'title': 'Total Customers', 'value': total_customers},
            {'title': 'Total Appointments', 'value': total_appointments},
            {'title': 'Pending', 'value': pending},
            {'title': 'Completed', 'value': completed}
        ],
        'popular': popular,
        'recent': appointments[-10:] if appointments else []
    })

@app.route('/api/ai/ask', methods=['POST'])
def ask_ai():
    question = request.json.get('question', '').lower()
    data = load_data()
    appointments = data['appointments']
    services_data = {s['name']: {'price': s['price'], 'material_cost': s.get('material_cost', 0)} for s in data['services']}
    materials = data.get('materials', {})
    
    total_revenue = 0
    total_material_cost = 0
    completed_count = 0
    
    for a in appointments:
        if a.get('status') == 'completed':
            service = services_data.get(a['service'])
            if service:
                total_revenue += service['price']
                total_material_cost += service['material_cost']
                completed_count += 1
    
    net_profit = total_revenue - total_material_cost
    
    if 'profit' in question or 'earn' in question or 'material' in question:
        answer = f"💰 Total Revenue: ${total_revenue:.2f} | Material Costs: ${total_material_cost:.2f} | Net Profit: ${net_profit:.2f}. Your margin is {((net_profit/total_revenue)*100) if total_revenue > 0 else 0:.1f}%. To increase profit, focus on {max(materials, key=lambda x: materials[x]['cost']) if materials else 'Nails'} which has highest material cost."
    elif 'popular' in question or 'best' in question:
        service_counts = {}
        for a in appointments:
            if a.get('status') == 'completed':
                service_counts[a['service']] = service_counts.get(a['service'], 0) + 1
        top = max(service_counts, key=service_counts.get) if service_counts else 'No data'
        answer = f"🎯 Your most popular service is {top} with {service_counts.get(top, 0)} bookings! Consider promoting your second-best services to balance demand."
    elif 'predict' in question or 'next' in question:
        monthly_avg = total_revenue / max(1, (datetime.now().month))
        answer = f"📈 Based on current data, next month projection: ${monthly_avg * 1.15:.2f} revenue and ${net_profit * 1.15:.2f} net profit. Book 15% more appointments to reach this goal!"
    else:
        answer = f"💡 You have {total_revenue:.2f} total revenue, {completed_count} completed appointments, and ${net_profit:.2f} net profit. Ask me about profits, popular services, or predictions!"
    
    return jsonify({'answer': answer})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("MEDICAL TOUCH CRM v2.0 - FULLY UPGRADED!")
    print("="*60)
    print("\nCustomer: http://127.0.0.1:5000")
    print("Admin:    http://127.0.0.1:5000/admin")
    print("\nAdmin Login: medicaltouch / admin123")
    print("\nNEW FEATURES:")
    print("  🔐 Admin Login Protection")
    print("  🤖 AI Double-Booking Prevention")
    print("  🎨 Most Wanted Services Wheel (colors!)")
    print("  📦 Materials Tracker per category")
    print("  💰 Net Profit Calculator (Revenue - Materials)")
    print("  🕐 12hr AM/PM Time Format")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
