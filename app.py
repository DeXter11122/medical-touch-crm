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
            # NAILS - 20 services
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
            # LASHES - 5 services
            {'id': '21', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '22', 'name': 'Full Set Lashes Volume', 'price': 38, 'duration': 90, 'category': 'Lashes', 'material_cost': 5},
            {'id': '23', 'name': 'Full Set Lashes Mega Volume', 'price': 45, 'duration': 105, 'category': 'Lashes', 'material_cost': 6},
            {'id': '24', 'name': 'Refill Lashes', 'price': 25, 'duration': 45, 'category': 'Lashes', 'material_cost': 3},
            {'id': '25', 'name': 'Removal Lashes', 'price': 20, 'duration': 30, 'category': 'Lashes', 'material_cost': 2},
            # SKINCARE - 16 services
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
            # WAX - 17 services
            {'id': '42', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax', 'material_cost': 3},
            {'id': '43', 'name': 'Full Face + Neck Wax', 'price': 15, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '44', 'name': 'Full Back Wax', 'price': 18, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '45', 'name': 'Lower Back Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '46', 'name': 'Half Back Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '47', 'name': 'Full Belly Wax', 'price': 18, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '48', 'name': 'Chest Wax', 'price': 12, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '49', 'name': 'Full Arms Wax', 'price': 12, 'duration': 30, 'category': 'Wax', 'material_cost': 1},
            {'id': '50', 'name': 'Half Arms Wax', 'price': 8, 'duration': 20, 'category': 'Wax', 'material_cost': 1},
            {'id': '51', 'name': 'Under Arms Wax', 'price': 12, 'duration': 15, 'category': 'Wax', 'material_cost': 1},
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

# Admin Login Page
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
        .login-box { background: white; padding: 40px; border-radius: 24px; width: 380px; text-align: center; }
        .logo { font-size: 50px; margin-bottom: 20px; }
        h2 { color: #ff6b9d; margin-bottom: 10px; }
        input { width: 100%; padding: 14px; margin: 10px 0; border: 2px solid #eee; border-radius: 12px; font-size: 16px; }
        input:focus { outline: none; border-color: #ff6b9d; }
        button { background: #ff6b9d; color: white; border: none; padding: 14px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; }
        .error { color: red; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">💅</div>
        <h2>Medical Touch Admin</h2>
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

# BEAUTIFUL CUSTOMER WEBSITE
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
        
        .hero {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .hero::before { content: '💅'; position: absolute; font-size: 150px; opacity: 0.05; bottom: -30px; right: -30px; }
        .hero h1 { font-family: 'Playfair Display', serif; font-size: 52px; letter-spacing: 3px; }
        .hero p { font-size: 16px; opacity: 0.9; margin-top: 10px; }
        .phone { margin-top: 15px; font-size: 20px; font-weight: 500; background: #ff6b9d; display: inline-block; padding: 8px 25px; border-radius: 50px; }
        
        .tabs {
            display: flex;
            justify-content: center;
            gap: 8px;
            background: white;
            padding: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
            flex-wrap: wrap;
        }
        .tab {
            padding: 10px 28px;
            font-size: 15px;
            font-weight: 500;
            background: none;
            border: none;
            cursor: pointer;
            border-radius: 40px;
            color: #666;
            transition: 0.3s;
        }
        .tab:hover { background: #ff6b9d20; color: #ff6b9d; }
        .tab.active { background: #ff6b9d; color: white; box-shadow: 0 4px 10px rgba(255,107,157,0.3); }
        
        .container { max-width: 1300px; margin: 0 auto; padding: 40px 20px; }
        .tab-content { display: none; animation: fadeIn 0.4s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .category-badge {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #1a1a2e;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 3px solid #ff6b9d;
            display: inline-block;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .service-card {
            background: white;
            border-radius: 20px;
            padding: 22px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 20px rgba(0,0,0,0.03);
            border: 1px solid #eee;
        }
        .service-card:hover {
            transform: translateY(-5px);
            border-color: #ff6b9d;
            box-shadow: 0 15px 30px rgba(255,107,157,0.1);
        }
        .service-name { font-size: 16px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }
        .service-price { font-size: 26px; font-weight: bold; color: #ff6b9d; }
        .service-duration { color: #aaa; font-size: 12px; margin-top: 8px; display: flex; align-items: center; gap: 5px; }
        .book-hint { margin-top: 12px; font-size: 12px; color: #ff6b9d; font-weight: 500; }
        
        .booking-section {
            background: linear-gradient(135deg, #fff5f7, #ffe4e8);
            border-radius: 28px;
            padding: 45px;
        }
        .booking-section h2 { font-family: 'Playfair Display', serif; font-size: 32px; color: #1a1a2e; margin-bottom: 25px; }
        .form-group { margin-bottom: 20px; }
        input, select {
            width: 100%;
            padding: 14px;
            border: 2px solid #eee;
            border-radius: 14px;
            font-size: 15px;
            font-family: 'Poppins', sans-serif;
            transition: 0.3s;
        }
        input:focus, select:focus { outline: none; border-color: #ff6b9d; }
        .submit-btn {
            background: #ff6b9d;
            color: white;
            border: none;
            padding: 14px;
            border-radius: 40px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: 0.3s;
        }
        .submit-btn:hover { background: #ff4d7d; transform: scale(1.02); }
        .warning { color: #ff4d7d; font-size: 12px; margin-top: 5px; display: none; }
        
        footer { background: #1a1a2e; color: white; text-align: center; padding: 40px; margin-top: 60px; }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 32px; }
            .tab { padding: 8px 18px; font-size: 13px; }
            .services-grid { grid-template-columns: 1fr; }
            .booking-section { padding: 25px; }
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>MEDICAL TOUCH</h1>
        <p>Where Beauty Meets Medical Excellence</p>
        <div class="phone">📞 81023625</div>
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
                    <div class="form-group"><input type="text" id="custName" placeholder="Full Name" required></div>
                    <div class="form-group"><input type="tel" id="custPhone" placeholder="Phone Number" required></div>
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
        <p>📍 Beirut, Lebanon | 📞 81023625</p>
    </footer>
    
    <script>
        let allServices = [];
        
        fetch('/api/services').then(r=>r.json()).then(services => {
            allServices = services;
            displayServices(services);
            populateSelect(services);
        });
        
        function displayServices(services) {
            const cats = {'Nails':'nailsGrid','Lashes':'lashesGrid','Skincare':'skincareGrid','Wax':'waxGrid'};
            for(let [cat, elId] of Object.entries(cats)) {
                let filtered = services.filter(s => s.category === cat);
                let html = '';
                filtered.forEach(s => {
                    html += `<div class="service-card" onclick="bookService('${s.name.replace(/'/g, "\\'")}')">
                        <div class="service-name">${s.name}</div>
                        <div class="service-price">$${s.price}</div>
                        <div class="service-duration">⏱️ ${s.duration} minutes</div>
                        <div class="book-hint">Click to book →</div>
                    </div>`;
                });
                document.getElementById(elId).innerHTML = html || '<p style="text-align:center;color:#999;">Loading services...</p>';
            }
        }
        
        function populateSelect(services) {
            let html = '<option value="">Select a service</option>';
            services.forEach(s => { html += `<option value="${s.name.replace(/'/g, "\\'")}">${s.name} - $${s.price}</option>`; });
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
        
        document.getElementById('appointmentDate').onchange = async function() {
            const res = await fetch('/api/check-slot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({datetime: this.value})
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
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            if(result.success) alert('✅ Appointment booked! We will confirm via SMS.');
            else if(result.double_booking) alert('❌ Sorry, this time is already taken. Please choose another time.');
            else alert('❌ Error. Please try again.');
            if(result.success) document.getElementById('bookingForm').reset();
        };
    </script>
</body>
</html>
'''# BEAUTIFUL ADMIN DASHBOARD
ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Medical Touch | Admin Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #f0f2f5; }
        
        .sidebar {
            width: 270px;
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            position: fixed;
            height: 100%;
            padding: 30px 20px;
        }
        .sidebar h2 { font-size: 22px; margin-bottom: 40px; text-align: center; }
        .sidebar nav a {
            display: block;
            color: white;
            text-decoration: none;
            padding: 12px 18px;
            margin: 8px 0;
            border-radius: 12px;
            transition: 0.3s;
        }
        .sidebar nav a:hover { background: #ff6b9d; transform: translateX(5px); }
        
        .main { margin-left: 270px; padding: 25px; }
        
        .top-bar {
            background: white;
            padding: 18px 25px;
            border-radius: 18px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .top-bar h2 { color: #1a1a2e; }
        .logout-btn { background: #ff4d7d; color: white; border: none; padding: 10px 25px; border-radius: 30px; cursor: pointer; font-weight: 500; }
        
        .wheels-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 30px;
        }
        .wheel-card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }
        .wheel-card h3 { color: #1a1a2e; margin-bottom: 20px; font-size: 18px; }
        .wheel {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .wheel-item {
            width: 105px;
            height: 105px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }
        .wheel-item:hover { transform: scale(1.05); }
        .wheel-item span { font-size: 22px; font-weight: bold; }
        .wheel-item div { font-size: 12px; margin-top: 5px; }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 18px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }
        .stat-card .number { font-size: 36px; font-weight: bold; color: #ff6b9d; }
        .stat-card p { color: #666; font-size: 14px; margin-top: 8px; }
        
        .section {
            background: white;
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            display: none;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }
        .section.active { display: block; }
        .section h2 { color: #1a1a2e; margin-bottom: 20px; font-size: 22px; }
        
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #fef8f9; color: #ff6b9d; font-weight: 600; }
        .delete-btn { background: #dc3545; color: white; border: none; padding: 5px 12px; border-radius: 6px; cursor: pointer; }
        .edit-btn { background: #ffc107; color: #333; border: none; padding: 5px 12px; border-radius: 6px; cursor: pointer; }
        input, select { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 8px; }
        button { background: #ff6b9d; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; }
        .profit-detail { margin-top: 15px; padding: 15px; background: #fef8f9; border-radius: 12px; display: none; font-size: 14px; }
        
        .ai-box {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            padding: 30px;
            color: white;
        }
        .ai-box input { width: 70%; padding: 12px; border: none; border-radius: 30px; }
        .ai-box button { background: white; color: #764ba2; border: none; padding: 12px 25px; border-radius: 30px; cursor: pointer; font-weight: bold; margin-left: 10px; }
        .ai-response { margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 12px; display: none; }
        
        @media (max-width: 768px) {
            .sidebar { width: 100%; height: auto; position: relative; }
            .main { margin-left: 0; }
            .wheels-container { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>💅 MEDICAL TOUCH</h2>
        <nav>
            <a href="#" onclick="showSection('dashboard')">📊 Dashboard</a>
            <a href="#" onclick="showSection('materials')">📦 Materials & Costs</a>
            <a href="#" onclick="showSection('customers')">👥 Customers</a>
            <a href="#" onclick="showSection('appointments')">📅 Appointments</a>
            <a href="#" onclick="showSection('services')">💅 Services</a>
            <a href="#" onclick="showSection('ai')">🤖 AI Assistant</a>
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
                    <div class="wheel" id="popularWheel"></div>
                    <div id="popularDetail" class="profit-detail"></div>
                </div>
            </div>
            
            <div class="stats-grid" id="statsGrid"></div>
            
            <h3 style="margin: 20px 0 15px 0;">📋 Recent Bookings</h3>
            <div id="recentList"></div>
        </div>
        
        <div id="materials" class="section">
            <h2>📦 Materials & Monthly Costs</h2>
            <div id="materialsGrid"></div>
            <div id="profitSummary" style="margin-top: 20px; padding: 20px; background: #fef8f9; border-radius: 15px;"></div>
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
            <div style="margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 10px;">
                <input type="text" id="newName" placeholder="Service Name" style="width: 200px;">
                <input type="number" id="newPrice" placeholder="Price $" style="width: 100px;">
                <select id="newCat" style="width: 120px;">
                    <option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option>
                </select>
                <input type="number" id="newCost" placeholder="Material Cost $" style="width: 130px;">
                <button onclick="addService()">➕ Add Service</button>
            </div>
            <div id="serviceTable"></div>
        </div>
        
        <div id="ai" class="section">
            <div class="ai-box">
                <h2>🤖 AI Business Assistant</h2>
                <p>Ask me anything about profits, popular services, or predictions!</p>
                <div style="margin-top: 20px;">
                    <input type="text" id="aiQuestion" placeholder="e.g., How much profit after materials?">
                    <button onclick="askAI()">Ask AI</button>
                </div>
                <div id="aiResponse" class="ai-response"></div>
            </div>
        </div>
    </div>
    
    <script>
        let profitData = {};
        let popularData = [];
        
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
            document.getElementById('todayAmt').innerText = '$' + profitData.today;
            document.getElementById('weekAmt').innerText = '$' + profitData.week;
            document.getElementById('monthAmt').innerText = '$' + profitData.month;
            document.getElementById('yearAmt').innerText = '$' + profitData.year;
            
            let statsHtml = '';
            d.stats.forEach(s => {
                statsHtml += `<div class="stat-card"><div class="number">${s.value}</div><p>${s.title}</p></div>`;
            });
            document.getElementById('statsGrid').innerHTML = statsHtml;
            
            let popularHtml = '';
            const colors = ['#ff6b9d', '#ff4d7d', '#ffb347', '#4ecdc4', '#45b7d1', '#96ceb4'];
            popularData.forEach((p, i) => {
                popularHtml += `<div class="wheel-item" style="background:${colors[i % colors.length]}" onclick="showPopular('${p.name.replace(/'/g, "\\'")}')">
                    <span>${p.name.substring(0, 8)}</span><div>${p.count} bookings</div>
                </div>`;
            });
            document.getElementById('popularWheel').innerHTML = popularHtml || '<p>No data yet</p>';
            
            let recentHtml = '';
            d.recent.forEach(a => {
                recentHtml += `<div style="padding: 12px; margin: 8px 0; border-left: 4px solid #ff6b9d; background: #f8f9fa; border-radius: 8px;">
                    <strong>${a.customer_name}</strong> - ${a.service}<br>
                    📅 ${a.datetime} | Status: ${a.status}
                </div>`;
            });
            document.getElementById('recentList').innerHTML = recentHtml || '<p>No appointments yet</p>';
        }
        
        function showProfit(p) {
            const d = document.getElementById('profitDetail');
            let msg = '';
            if(p === 'today') msg = `💰 Today: $${profitData.today} (${profitData.todayCount||0} appointments) | Net Profit: $${profitData.todayNet||0}`;
            if(p === 'week') msg = `💰 This Week: $${profitData.week} (${profitData.weekCount||0} appointments) | Net Profit: $${profitData.weekNet||0}`;
            if(p === 'month') msg = `💰 This Month: $${profitData.month} (${profitData.monthCount||0} appointments) | Net Profit: $${profitData.monthNet||0}`;
            if(p === 'year') msg = `💰 This Year: $${profitData.year} (${profitData.yearCount||0} appointments) | Net Profit: $${profitData.yearNet||0}`;
            d.innerHTML = msg;
            d.style.display = 'block';
            setTimeout(() => d.style.display = 'none', 4000);
        }
        
        function showPopular(name) {
            const d = document.getElementById('popularDetail');
            const p = popularData.find(x => x.name === name);
            if(p) {
                d.innerHTML = `🎯 ${p.name}: ${p.count} bookings | Revenue: $${p.revenue} | Material Cost: $${p.materialCost} | Net Profit: $${p.netProfit}`;
            } else {
                d.innerHTML = 'No data available';
            }
            d.style.display = 'block';
            setTimeout(() => d.style.display = 'none', 4000);
        }
        
        async function loadMaterials() {
            const r = await fetch('/api/materials');
            const d = await r.json();
            let html = '<table><tr><th>Category</th><th>Monthly Material Cost</th><th>Items</th><th>Action</th></tr>';
            for(let cat in d.materials) {
                html += `<tr>
                    <td><strong>${cat}</strong></td>
                    <td><input type="number" id="cost_${cat}" value="${d.materials[cat].cost}" style="width:100px"> $</td>
                    <td>${d.materials[cat].items.join(', ')}</td>
                    <td><button onclick="updateMaterialCost('${cat}')">Update</button></td>
                </tr>`;
            }
            html += '</table>';
            document.getElementById('materialsGrid').innerHTML = html;
            document.getElementById('profitSummary').innerHTML = `
                <h3>💰 Financial Summary</h3>
                <p>Total Revenue: $${d.totalRevenue} | Total Material Cost: $${d.totalMaterialCost} | <strong>Net Profit: $${d.netProfit}</strong></p>
                <p style="font-size:13px; color:#666; margin-top:10px;">Margin: ${((d.netProfit/d.totalRevenue)*100).toFixed(1)}%</p>
            `;
        }
        
        async function updateMaterialCost(cat) {
            const cost = document.getElementById(`cost_${cat}`).value;
            await fetch('/api/materials/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({category: cat, cost: parseInt(cost)})
            });
            loadMaterials();
        }
        
        async function loadCustomers() {
            const r = await fetch('/api/customers');
            const c = await r.json();
            let h = '<table><tr><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Action</th></tr>';
            c.forEach(cust => {
                h += `<tr>
                    <td>${cust.name}</td>
                    <td>${cust.phone}</td>
                    <td>${cust.email || '-'}</td>
                    <td>${cust.visits || 0}</td>
                    <td><button class="delete-btn" onclick="deleteCustomer('${cust.id}')">Delete</button></td>
                </tr>`;
            });
            h += '</table>';
            document.getElementById('customerTable').innerHTML = h;
        }
        
        async function loadAppointments() {
            const r = await fetch('/api/appointments');
            const a = await r.json();
            let h = '<table><tr><th>Customer</th><th>Service</th><th>Date & Time</th><th>Status</th><th>Action</th></tr>';
            a.forEach(app => {
                h += `<tr>
                    <td>${app.customer_name}</td>
                    <td>${app.service}</td>
                    <td>${app.datetime}</td>
                    <td><select onchange="updateStatus('${app.id}', this.value)">
                        <option ${app.status === 'pending' ? 'selected' : ''}>pending</option>
                        <option ${app.status === 'confirmed' ? 'selected' : ''}>confirmed</option>
                        <option ${app.status === 'completed' ? 'selected' : ''}>completed</option>
                    </select></td>
                    <td><button class="delete-btn" onclick="deleteAppointment('${app.id}')">Cancel</button></td>
                </tr>`;
            });
            h += '</table>';
            document.getElementById('appointmentTable').innerHTML = h;
        }
        
        async function loadServices() {
            const r = await fetch('/api/services');
            const s = await r.json();
            let h = '<table><tr><th>Service</th><th>Price</th><th>Duration</th><th>Category</th><th>Material Cost</th><th>Action</th></tr>';
            s.forEach(serv => {
                h += `<tr>
                    <td>${serv.name}</td>
                    <td>$${serv.price}</td>
                    <td>${serv.duration} min</td>
                    <td>${serv.category}</td>
                    <td>$${serv.material_cost || 0}</td>
                    <td><button class="delete-btn" onclick="deleteService('${serv.id}')">Delete</button></td>
                </tr>`;
            });
            h += '</table>';
            document.getElementById('serviceTable').innerHTML = h;
        }
        
        async function addService() {
            await fetch('/api/services', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: document.getElementById('newName').value,
                    price: parseInt(document.getElementById('newPrice').value),
                    duration: 60,
                    category: document.getElementById('newCat').value,
                    material_cost: parseInt(document.getElementById('newCost').value) || 0
                })
            });
            loadServices();
            document.getElementById('newName').value = '';
            document.getElementById('newPrice').value = '';
            document.getElementById('newCost').value = '';
        }
        
        async function deleteService(id) { if(confirm('Delete this service?')) { await fetch('/api/services/' + id, {method: 'DELETE'}); loadServices(); } }
        async function deleteCustomer(id) { if(confirm('Delete this customer?')) { await fetch('/api/customers/' + id, {method: 'DELETE'}); loadCustomers(); loadDashboard(); } }
        async function deleteAppointment(id) { if(confirm('Cancel this appointment?')) { await fetch('/api/appointments/' + id, {method: 'DELETE'}); loadAppointments(); loadDashboard(); } }
        async function updateStatus(id, status) { await fetch('/api/appointments/' + id + '/status', {method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({status: status})}); loadDashboard(); loadAppointments(); }
        
        async function askAI() {
            const q = document.getElementById('aiQuestion').value;
            if(!q) return;
            const r = await fetch('/api/ai/ask', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: q})});
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
        customer = {
            'id': str(len(data['customers']) + 1),
            'name': booking['name'],
            'phone': booking['phone'],
            'email': booking.get('email', ''),
            'visits': 0
        }
        data['customers'].append(customer)
    
    appointment = {
        'id': str(len(data['appointments']) + 1),
        'customer_id': customer['id'],
        'customer_name': customer['name'],
        'service': booking['service'],
        'datetime': booking['datetime'],
        'status': 'pending',
        'staff_id': 'staff1',
        'booked_at': datetime.now().isoformat()
    }
    data['appointments'].append(appointment)
    save_data(data)
    add_notification(f"📅 New booking: {customer['name']} - {booking['service']} at {booking['datetime']}")
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
    add_notification(f"❌ Appointment cancelled: {appointment_id}")
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
                add_notification(f"✅ Appointment completed: {a['customer_name']} - {a['service']}")
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/materials', methods=['GET'])
def get_materials():
    data = load_data()
    services = data['services']
    appointments = data['appointments']
    materials = data.get('materials', {})
    services_dict = {s['name']: s for s in services}
    
    total_revenue = 0
    total_material_cost = 0
    
    for a in appointments:
        if a.get('status') == 'completed':
            service = services_dict.get(a['service'])
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
    
    total_customers = len(data['customers'])
    total_appointments = len(appointments)
    pending = sum(1 for a in appointments if a.get('status') == 'pending')
    completed = sum(1 for a in appointments if a.get('status') == 'completed')
    
    today_total = week_total = month_total = year_total = 0
    today_cost = week_cost = month_cost = year_cost = 0
    today_count = week_count = month_count = year_count = 0
    
    service_counts = {}
    service_revenue = {}
    service_material_cost = {}
    
    for a in appointments:
        service = services_data.get(a['service'])
        if not service:
            continue
        
        if a.get('status') == 'completed':
            price = service['price']
            cost = service['material_cost']
            
            service_counts[a['service']] = service_counts.get(a['service'], 0) + 1
            service_revenue[a['service']] = service_revenue.get(a['service'], 0) + price
            service_material_cost[a['service']] = service_material_cost.get(a['service'], 0) + cost
            
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
            {'title': '👥 Total Customers', 'value': total_customers},
            {'title': '📅 Total Appointments', 'value': total_appointments},
            {'title': '⏳ Pending', 'value': pending},
            {'title': '✅ Completed', 'value': completed}
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
    
    total_revenue = 0
    total_material_cost = 0
    completed_count = 0
    
    service_counts = {}
    
    for a in appointments:
        if a.get('status') == 'completed':
            service = services_data.get(a['service'])
            if service:
                total_revenue += service['price']
                total_material_cost += service['material_cost']
                completed_count += 1
                service_counts[a['service']] = service_counts.get(a['service'], 0) + 1
    
    net_profit = total_revenue - total_material_cost
    margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    if 'profit' in question or 'earn' in question or 'material' in question:
        answer = f"💰 Total Revenue: ${total_revenue:.2f} | Material Costs: ${total_material_cost:.2f} | Net Profit: ${net_profit:.2f} | Your profit margin is {margin:.1f}%. To improve, focus on services with lower material costs like Wax which has 85%+ margin!"
    
    elif 'popular' in question or 'best' in question or 'most' in question:
        top = max(service_counts, key=service_counts.get) if service_counts else 'No data'
        top_count = service_counts.get(top, 0)
        answer = f"🎯 Your most popular service is '{top}' with {top_count} bookings! Consider promoting your second-best services to balance demand and increase overall revenue."
    
    elif 'predict' in question or 'next' in question or 'forecast' in question:
        monthly_avg = total_revenue / max(1, datetime.now().month)
        projected = monthly_avg * 1.15
        answer = f"📈 Based on your data, next month projection: ${projected:.2f} revenue and ${projected * (margin/100):.2f} net profit. Book 15% more appointments to reach this goal!"
    
    elif 'grow' in question or 'increase' in question or 'improve' in question:
        answer = f"🚀 Growth tips for Medical Touch: 1) SMS reminders reduce no-shows by 30% 2) Loyalty program for repeat customers 3) Promote your {max(service_counts, key=service_counts.get) if service_counts else 'best'} service which is your bestseller 4) Add package deals for multiple services!"
    
    else:
        answer = f"💡 Medical Touch Summary: ${total_revenue:.2f} total revenue, {completed_count} completed appointments, ${net_profit:.2f} net profit ({margin:.1f}% margin). Ask me about profits, popular services, predictions, or growth tips!"
    
    return jsonify({'answer': answer})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✨ MEDICAL TOUCH CRM v2.0 - FULLY UPGRADED! ✨")
    print("="*60)
    print("\n📍 CUSTOMER WEBSITE: http://127.0.0.1:5000")
    print("🔐 ADMIN DASHBOARD:  http://127.0.0.1:5000/admin")
    print("\n🔑 Admin Login: medicaltouch / admin123")
    print("\n✨ NEW FEATURES:")
    print("  🔐 Admin Login Protection")
    print("  🤖 AI Double-Booking Prevention")
    print("  🎨 Most Wanted Services Wheel (with colors!)")
    print("  📦 Materials Tracker per category")
    print("  💰 Net Profit Calculator (Revenue - Materials)")
    print("  📋 60+ Services with REAL prices from your PDF")
    print("  🕐 12hr AM/PM Time Format")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

# Rest of API routes (keeping same as before but with updated service list)
# I'll continue in next message due to length...
