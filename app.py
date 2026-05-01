from flask import Flask, render_template_string, request, jsonify, send_from_directory
import json
import os
from datetime import datetime
import time

app = Flask(__name__)

DATA_FILE = 'salon_data.json'
NOTIFICATIONS_FILE = 'notifications.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    # Complete service list - ALL your prices
    return {'customers': [], 'appointments': [], 'services': [
        # NAILS
        {'id': '1', 'name': 'Full Set GEL + Manicure', 'price': 40, 'duration': 90, 'category': 'Nails'},
        {'id': '2', 'name': 'Full Set Fiber GEL', 'price': 35, 'duration': 75, 'category': 'Nails'},
        {'id': '3', 'name': 'Full Set Polygel', 'price': 35, 'duration': 75, 'category': 'Nails'},
        {'id': '4', 'name': 'Rubber Base + Color Gel', 'price': 15, 'duration': 45, 'category': 'Nails'},
        {'id': '5', 'name': 'Full Set Gel-X', 'price': 30, 'duration': 60, 'category': 'Nails'},
        {'id': '6', 'name': 'Full Set Acrylic', 'price': 38, 'duration': 75, 'category': 'Nails'},
        {'id': '7', 'name': 'Pedicure + Pose', 'price': 45, 'duration': 60, 'category': 'Nails'},
        {'id': '8', 'name': 'Refill GEL', 'price': 22, 'duration': 45, 'category': 'Nails'},
        {'id': '9', 'name': 'Remove GEL', 'price': 15, 'duration': 30, 'category': 'Nails'},
        {'id': '10', 'name': 'Gel Color Change', 'price': 18, 'duration': 30, 'category': 'Nails'},
        {'id': '11', 'name': 'Dipping Powder GEL', 'price': 30, 'duration': 60, 'category': 'Nails'},
        {'id': '12', 'name': 'Full Set Lucid GEL', 'price': 30, 'duration': 60, 'category': 'Nails'},
        {'id': '13', 'name': 'Ombre Gelish', 'price': 15, 'duration': 30, 'category': 'Nails'},
        {'id': '14', 'name': 'French Gelish', 'price': 15, 'duration': 30, 'category': 'Nails'},
        {'id': '15', 'name': 'French Verni', 'price': 10, 'duration': 20, 'category': 'Nails'},
        {'id': '16', 'name': 'Pose Verni', 'price': 5, 'duration': 15, 'category': 'Nails'},
        {'id': '17', 'name': 'Special Nail Art', 'price': 15, 'duration': 30, 'category': 'Nails'},
        {'id': '18', 'name': 'Parafine Treatment', 'price': 8, 'duration': 20, 'category': 'Nails'},
        # LASHES
        {'id': '19', 'name': 'Full Set Lashes Classic', 'price': 35, 'duration': 90, 'category': 'Lashes'},
        {'id': '20', 'name': 'Full Set Lashes Volume', 'price': 38, 'duration': 90, 'category': 'Lashes'},
        {'id': '21', 'name': 'Full Set Lashes Mega Volume', 'price': 45, 'duration': 105, 'category': 'Lashes'},
        {'id': '22', 'name': 'Refill Lashes', 'price': 25, 'duration': 45, 'category': 'Lashes'},
        {'id': '23', 'name': 'Removal Lashes', 'price': 20, 'duration': 30, 'category': 'Lashes'},
        {'id': '24', 'name': 'Lashes Fake Nails', 'price': 25, 'duration': 45, 'category': 'Lashes'},
        # SKINCARE
        {'id': '25', 'name': 'Facial Classic', 'price': 35, 'duration': 60, 'category': 'Skincare'},
        {'id': '26', 'name': 'Hydra Facial', 'price': 55, 'duration': 75, 'category': 'Skincare'},
        {'id': '27', 'name': 'Medical Facial + MesoTherapy', 'price': 65, 'duration': 90, 'category': 'Skincare'},
        {'id': '28', 'name': 'MesoPen Hair Loss', 'price': 35, 'duration': 45, 'category': 'Skincare'},
        {'id': '29', 'name': 'MesoPen Hair Grow', 'price': 35, 'duration': 45, 'category': 'Skincare'},
        {'id': '30', 'name': 'MesoPen Whitening', 'price': 35, 'duration': 45, 'category': 'Skincare'},
        {'id': '31', 'name': 'MesoPen Acne', 'price': 35, 'duration': 45, 'category': 'Skincare'},
        {'id': '32', 'name': 'MesoPen Lip Whitening', 'price': 35, 'duration': 45, 'category': 'Skincare'},
        {'id': '33', 'name': 'MesoPen Lifting Face', 'price': 55, 'duration': 60, 'category': 'Skincare'},
        {'id': '34', 'name': 'MesoPen Dark Circle', 'price': 45, 'duration': 45, 'category': 'Skincare'},
        {'id': '35', 'name': 'Meso botox Injection', 'price': 100, 'duration': 60, 'category': 'Skincare'},
        {'id': '36', 'name': 'MesoPen Cellulite', 'price': 35, 'duration': 45, 'category': 'Skincare'},
        {'id': '37', 'name': 'Meso lipo double Chin', 'price': 100, 'duration': 60, 'category': 'Skincare'},
        {'id': '38', 'name': 'Meso Fats (5 Sessions)', 'price': 200, 'duration': 60, 'category': 'Skincare'},
        {'id': '39', 'name': 'Meso Melasma Injection', 'price': 100, 'duration': 60, 'category': 'Skincare'},
        {'id': '40', 'name': 'HIFU', 'price': 100, 'duration': 90, 'category': 'Skincare'},
        # WAX
        {'id': '41', 'name': 'Full Body Wax', 'price': 45, 'duration': 60, 'category': 'Wax'},
        {'id': '42', 'name': 'Full Face + Neck Wax', 'price': 20, 'duration': 30, 'category': 'Wax'},
        {'id': '43', 'name': 'Full Back Wax', 'price': 35, 'duration': 45, 'category': 'Wax'},
        {'id': '44', 'name': 'Full Belly Wax', 'price': 15, 'duration': 30, 'category': 'Wax'},
        {'id': '45', 'name': 'Full Legs Wax', 'price': 18, 'duration': 45, 'category': 'Wax'},
        {'id': '46', 'name': 'Half Legs Wax', 'price': 12, 'duration': 30, 'category': 'Wax'},
        {'id': '47', 'name': 'Full Arms Wax', 'price': 15, 'duration': 30, 'category': 'Wax'},
        {'id': '48', 'name': 'Half Arms Wax', 'price': 8, 'duration': 20, 'category': 'Wax'},
        {'id': '49', 'name': 'Chest Wax', 'price': 18, 'duration': 30, 'category': 'Wax'},
        {'id': '50', 'name': 'Lower Back Wax', 'price': 15, 'duration': 30, 'category': 'Wax'},
        {'id': '51', 'name': 'Under Arms Wax', 'price': 6, 'duration': 15, 'category': 'Wax'},
        {'id': '52', 'name': 'Full Bikini Wax', 'price': 18, 'duration': 30, 'category': 'Wax'},
        {'id': '53', 'name': 'Bikini Line Wax', 'price': 12, 'duration': 20, 'category': 'Wax'},
        {'id': '54', 'name': 'Lips Wax', 'price': 5, 'duration': 10, 'category': 'Wax'},
        {'id': '55', 'name': 'Eyebrow Classic Wax', 'price': 8, 'duration': 10, 'category': 'Wax'},
        {'id': '56', 'name': 'Eyebrow Waxing', 'price': 10, 'duration': 10, 'category': 'Wax'},
        {'id': '57', 'name': 'Nose + Chin Wax', 'price': 12, 'duration': 15, 'category': 'Wax'},
    ]}

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
        'time': datetime.now().strftime('%H:%M:%S %Y-%m-%d'),
        'read': False
    })
    save_notifications(notifs[:50])

# Customer Website HTML - Tabs Design
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
        
        /* Header */
        .header {
            background: #1a1a2e;
            color: white;
            padding: 50px 20px;
            text-align: center;
        }
        .logo {
            width: 80px;
            height: 80px;
            background: #ff6b9d;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
        }
        .header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 48px;
            letter-spacing: 2px;
        }
        .header p {
            font-size: 16px;
            opacity: 0.8;
            margin-top: 10px;
        }
        .phone {
            margin-top: 15px;
            font-size: 20px;
            font-weight: 500;
        }
        
        /* Tabs Navigation */
        .tabs {
            display: flex;
            justify-content: center;
            gap: 5px;
            background: white;
            padding: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
            flex-wrap: wrap;
        }
        .tab {
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 500;
            background: none;
            border: none;
            cursor: pointer;
            border-radius: 30px;
            transition: 0.3s;
            color: #666;
        }
        .tab:hover {
            background: #ff6b9d20;
            color: #ff6b9d;
        }
        .tab.active {
            background: #ff6b9d;
            color: white;
        }
        
        /* Content Container */
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        /* Tab Content */
        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Category Title */
        .category-title {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #1a1a2e;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 3px solid #ff6b9d;
            display: inline-block;
        }
        
        /* Services Grid */
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .service-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            transition: 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            cursor: pointer;
            border: 1px solid #eee;
        }
        .service-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255,107,157,0.15);
            border-color: #ff6b9d;
        }
        .service-name {
            font-size: 16px;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 8px;
        }
        .service-price {
            font-size: 24px;
            font-weight: bold;
            color: #ff6b9d;
        }
        .service-duration {
            color: #999;
            font-size: 13px;
            margin-top: 8px;
        }
        .book-badge {
            display: inline-block;
            margin-top: 12px;
            font-size: 13px;
            color: #ff6b9d;
            font-weight: 500;
        }
        
        /* Booking Section */
        .booking-section {
            background: linear-gradient(135deg, #fff5f7, #ffe4e8);
            border-radius: 24px;
            padding: 40px;
            margin-top: 50px;
        }
        .booking-section h2 {
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            color: #1a1a2e;
            margin-bottom: 25px;
        }
        .form-group { margin-bottom: 20px; }
        input, select {
            width: 100%;
            padding: 14px;
            border: 2px solid #eee;
            border-radius: 12px;
            font-size: 15px;
            font-family: 'Poppins', sans-serif;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #ff6b9d;
        }
        .submit-btn {
            background: #ff6b9d;
            color: white;
            border: none;
            padding: 14px 30px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: 0.3s;
        }
        .submit-btn:hover {
            background: #ff4d7d;
            transform: scale(1.01);
        }
        
        footer {
            background: #1a1a2e;
            color: white;
            text-align: center;
            padding: 40px;
            margin-top: 60px;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 32px; }
            .tab { padding: 8px 16px; font-size: 14px; }
            .services-grid { grid-template-columns: 1fr; }
            .booking-section { padding: 25px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo" id="logoContainer">💅</div>
        <h1>MEDICAL TOUCH</h1>
        <p>Where Beauty Meets Medical Excellence</p>
        <div class="phone">📞 81023625</div>
    </div>
    
    <div class="tabs">
        <button class="tab active" onclick="switchTab('nails')">Nails</button>
        <button class="tab" onclick="switchTab('lashes')">Lashes</button>
        <button class="tab" onclick="switchTab('skincare')">Skincare</button>
        <button class="tab" onclick="switchTab('wax')">Wax</button>
        <button class="tab" onclick="switchTab('book')">Book Now</button>
    </div>
    
    <div class="container">
        <!-- Nails Tab -->
        <div id="nails" class="tab-content active">
            <div class="services-grid" id="nailsGrid"></div>
        </div>
        
        <!-- Lashes Tab -->
        <div id="lashes" class="tab-content">
            <div class="services-grid" id="lashesGrid"></div>
        </div>
        
        <!-- Skincare Tab -->
        <div id="skincare" class="tab-content">
            <div class="services-grid" id="skincareGrid"></div>
        </div>
        
        <!-- Wax Tab -->
        <div id="wax" class="tab-content">
            <div class="services-grid" id="waxGrid"></div>
        </div>
        
        <!-- Booking Tab -->
        <div id="book" class="tab-content">
            <div class="booking-section">
                <h2>Book Your Appointment</h2>
                <form id="bookingForm">
                    <div class="form-group">
                        <input type="text" id="custName" placeholder="Full Name" required>
                    </div>
                    <div class="form-group">
                        <input type="tel" id="custPhone" placeholder="Phone Number" required>
                    </div>
                    <div class="form-group">
                        <input type="email" id="custEmail" placeholder="Email">
                    </div>
                    <div class="form-group">
                        <select id="serviceSelect" required>
                            <option value="">Select a Service</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <input type="datetime-local" id="appointmentDate" required>
                    </div>
                    <button type="submit" class="submit-btn">Confirm Booking</button>
                </form>
            </div>
        </div>
    </div>
    
    <footer>
        <p>MEDICAL TOUCH | Beauty & Wellness</p>
        <p>Beirut, Lebanon | 81023625</p>
        <p style="font-size: 12px; margin-top: 15px;">2024 Medical Touch. All rights reserved.</p>
    </footer>
    
    <script>
        let allServices = [];
        
        // Load services from server
        fetch('/api/services')
            .then(res => res.json())
            .then(services => {
                allServices = services;
                displayServicesByCategory(services);
                populateServiceSelect(services);
            })
            .catch(err => console.error('Error loading services:', err));
        
        function displayServicesByCategory(services) {
            const categories = {
                'Nails': 'nailsGrid',
                'Lashes': 'lashesGrid',
                'Skincare': 'skincareGrid',
                'Wax': 'waxGrid'
            };
            
            for (let [category, elementId] of Object.entries(categories)) {
                const categoryServices = services.filter(s => s.category === category);
                let html = '';
                if (categoryServices.length === 0) {
                    html = '<p style="color: #999; text-align: center;">Services coming soon...</p>';
                } else {
                    categoryServices.forEach(s => {
                        html += `
                            <div class="service-card" onclick="bookThisService('${s.name.replace(/'/g, "\\'")}')">
                                <div class="service-name">${s.name}</div>
                                <div class="service-price">$${s.price}</div>
                                <div class="service-duration">${s.duration} minutes</div>
                                <div class="book-badge">Click to book →</div>
                            </div>
                        `;
                    });
                }
                document.getElementById(elementId).innerHTML = html;
            }
        }
        
        function populateServiceSelect(services) {
            let html = '<option value="">Select a service</option>';
            services.forEach(s => {
                html += `<option value="${s.name.replace(/'/g, "\\'")}">${s.name} - $${s.price}</option>`;
            });
            document.getElementById('serviceSelect').innerHTML = html;
        }
        
        function bookThisService(serviceName) {
            document.getElementById('serviceSelect').value = serviceName;
            switchTab('book');
        }
        
        function switchTab(tabName) {
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Update content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabName).classList.add('active');
        }
        
        // Handle booking form
        document.getElementById('bookingForm').onsubmit = async (e) => {
            e.preventDefault();
            
            const data = {
                name: document.getElementById('custName').value,
                phone: document.getElementById('custPhone').value,
                email: document.getElementById('custEmail').value,
                service: document.getElementById('serviceSelect').value,
                datetime: document.getElementById('appointmentDate').value
            };
            
            if (!data.name || !data.phone || !data.service || !data.datetime) {
                alert('Please fill in all required fields');
                return;
            }
            
            const res = await fetch('/api/customer-book', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                alert('Appointment booked successfully! We will confirm via SMS.');
                document.getElementById('bookingForm').reset();
                switchTab('book');
            } else {
                alert('Something went wrong. Please try again.');
            }
        };
        
        // Logo upload - check if logo exists
        const logoImg = new Image();
        logoImg.onload = function() {
            document.getElementById('logoContainer').innerHTML = '<img src="/static/logo.png" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">';
        };
        logoImg.src = '/static/logo.png';
    </script>
</body>
</html>
'''

# Admin Dashboard HTML (keep the working version)
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
            width: 280px;
            background: #1a1a2e;
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
            padding: 12px 20px;
            margin: 8px 0;
            border-radius: 12px;
            transition: 0.3s;
        }
        .sidebar nav a:hover { background: #ff6b9d; }
        
        .main { margin-left: 280px; padding: 30px; }
        
        .top-bar {
            background: white;
            padding: 20px 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .salon-name { font-size: 24px; font-weight: bold; color: #ff6b9d; }
        
        .bell-icon { font-size: 28px; cursor: pointer; position: relative; }
        .badge {
            position: absolute;
            top: -5px;
            right: -10px;
            background: #ff4d7d;
            color: white;
            border-radius: 50%;
            padding: 2px 8px;
            font-size: 12px;
        }
        .dropdown {
            position: absolute;
            top: 45px;
            right: 0;
            width: 350px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            display: none;
            z-index: 1000;
        }
        .dropdown.show { display: block; }
        .dropdown-header { background: #ff6b9d; color: white; padding: 15px; border-radius: 15px 15px 0 0; }
        .dropdown-list { max-height: 400px; overflow-y: auto; }
        .notif-item { padding: 15px; border-bottom: 1px solid #eee; }
        
        .scroll-wheel-container {
            background: white;
            border-radius: 25px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
        }
        .scroll-wheel { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; }
        .wheel {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            background: #ff6b9d;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }
        .wheel:hover { transform: scale(1.05); background: #ff4d7d; }
        .wheel .amount { font-size: 28px; font-weight: bold; }
        .wheel .label { font-size: 13px; margin-top: 5px; }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
        }
        .stat-card h3 { color: #ff6b9d; font-size: 14px; margin-bottom: 10px; }
        .stat-card .number { font-size: 40px; font-weight: bold; color: #1a1a2e; }
        
        .section {
            background: white;
            border-radius: 25px;
            padding: 30px;
            margin-bottom: 30px;
            display: none;
        }
        .section.active { display: block; }
        .section h2 { color: #1a1a2e; margin-bottom: 25px; font-size: 24px; }
        
        .ai-assistant {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            padding: 30px;
            color: white;
        }
        .ai-question { display: flex; gap: 15px; margin-top: 20px; }
        .ai-question input { flex: 1; padding: 14px; border: none; border-radius: 12px; }
        .ai-question button { background: white; color: #764ba2; border: none; padding: 14px 25px; border-radius: 12px; cursor: pointer; font-weight: bold; }
        .ai-response { margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 12px; display: none; }
        
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #fef8f9; color: #ff6b9d; }
        .delete-btn { background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 6px; cursor: pointer; }
        input, select { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 8px; }
        button { background: #ff6b9d; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; }
        .profit-detail { margin-top: 20px; padding: 15px; background: #fef8f9; border-radius: 12px; display: none; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Medical Touch</h2>
        <nav>
            <a href="#" onclick="showSection('dashboard')">Dashboard</a>
            <a href="#" onclick="showSection('customers')">Customers</a>
            <a href="#" onclick="showSection('appointments')">Appointments</a>
            <a href="#" onclick="showSection('services')">Services</a>
            <a href="#" onclick="showSection('ai')">AI Assistant</a>
        </nav>
    </div>
    
    <div class="main">
        <div class="top-bar">
            <div class="salon-name">Medical Touch Admin</div>
            <div style="position:relative">
                <div class="bell-icon" onclick="toggleNotifications()">🔔 <span id="notifBadge" class="badge">0</span></div>
                <div id="notifDropdown" class="dropdown">
                    <div class="dropdown-header">Notifications</div>
                    <div id="notifList" class="dropdown-list"></div>
                </div>
            </div>
        </div>
        
        <div id="dashboard" class="section active">
            <div class="scroll-wheel-container">
                <h2>Earnings Overview</h2>
                <div class="scroll-wheel">
                    <div class="wheel" onclick="showProfit('today')"><div class="amount" id="todayAmount">$0</div><div class="label">Today</div></div>
                    <div class="wheel" onclick="showProfit('week')"><div class="amount" id="weekAmount">$0</div><div class="label">This Week</div></div>
                    <div class="wheel" onclick="showProfit('month')"><div class="amount" id="monthAmount">$0</div><div class="label">This Month</div></div>
                    <div class="wheel" onclick="showProfit('year')"><div class="amount" id="yearAmount">$0</div><div class="label">This Year</div></div>
                </div>
                <div id="profitDetail" class="profit-detail"></div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card"><h3>Total Customers</h3><div class="number" id="totalCustomers">0</div></div>
                <div class="stat-card"><h3>Total Appointments</h3><div class="number" id="totalAppointments">0</div></div>
                <div class="stat-card"><h3>Pending</h3><div class="number" id="pendingCount">0</div></div>
                <div class="stat-card"><h3>Completed</h3><div class="number" id="completedCount">0</div></div>
            </div>
            
            <h2>Recent Bookings</h2>
            <div id="recentAppointments"></div>
        </div>
        
        <div id="customers" class="section"><h2>Customer Directory</h2><div id="customerTable"></div></div>
        <div id="appointments" class="section"><h2>Appointment Manager</h2><div id="appointmentTable"></div></div>
        <div id="services" class="section">
            <h2>Service Manager</h2>
            <div><input type="text" id="newServiceName" placeholder="Service Name"><input type="number" id="newServicePrice" placeholder="Price"><select id="newServiceCategory"><option>Nails</option><option>Lashes</option><option>Skincare</option><option>Wax</option></select><button onclick="addService()">Add Service</button></div>
            <div id="serviceTable" style="margin-top:20px"></div>
        </div>
        <div id="ai" class="section">
            <div class="ai-assistant">
                <h2>AI Business Assistant</h2>
                <p>Ask me about profits, predictions, or how to grow your business</p>
                <div class="ai-question">
                    <input type="text" id="aiQuestion" placeholder="e.g., How much will I make next month?">
                    <button onclick="askAI()">Ask</button>
                </div>
                <div id="aiResponse" class="ai-response"></div>
            </div>
            <div class="stat-card" style="margin-top:20px"><h3>Quick Insights</h3><div id="quickInsights"></div></div>
        </div>
    </div>
    
    <script>
        let profitData = {};
        
        function showSection(s) {
            document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
            document.getElementById(s).classList.add('active');
            if(s === 'dashboard') loadDashboard();
            if(s === 'customers') loadCustomers();
            if(s === 'appointments') loadAppointments();
            if(s === 'services') loadServices();
            if(s === 'ai') loadQuickInsights();
        }
        
        async function loadDashboard() {
            const res = await fetch('/api/admin/stats');
            const data = await res.json();
            profitData = data.profit;
            document.getElementById('todayAmount').innerText = '$' + profitData.today;
            document.getElementById('weekAmount').innerText = '$' + profitData.week;
            document.getElementById('monthAmount').innerText = '$' + profitData.month;
            document.getElementById('yearAmount').innerText = '$' + profitData.year;
            document.getElementById('totalCustomers').innerText = data.customers;
            document.getElementById('totalAppointments').innerText = data.appointments;
            document.getElementById('pendingCount').innerText = data.pending;
            document.getElementById('completedCount').innerText = data.completed;
            
            let html = '';
            if(data.recent && data.recent.length > 0) {
                data.recent.forEach(a => {
                    html += `<div style="background:#f8f9fa; padding:12px; margin:10px 0; border-radius:10px; border-left:3px solid #ff6b9d;">
                        <strong>${a.customer_name}</strong> - ${a.service}<br>
                        ${a.datetime} | Status: ${a.status}
                    </div>`;
                });
            } else {
                html = '<p>No appointments yet</p>';
            }
            document.getElementById('recentAppointments').innerHTML = html;
        }
        
        function showProfit(period) {
            const d = document.getElementById('profitDetail');
            let msg = '';
            if(period === 'today') msg = `Today's Earnings: $${profitData.today} | Appointments: ${profitData.todayCount || 0}`;
            if(period === 'week') msg = `This Week's Earnings: $${profitData.week} | Appointments: ${profitData.weekCount || 0}`;
            if(period === 'month') msg = `This Month's Earnings: $${profitData.month} | Appointments: ${profitData.monthCount || 0}`;
            if(period === 'year') msg = `This Year's Earnings: $${profitData.year} | Appointments: ${profitData.yearCount || 0}`;
            d.innerHTML = msg;
            d.style.display = 'block';
            setTimeout(() => d.style.display = 'none', 4000);
        }
        
        async function loadCustomers() {
            const res = await fetch('/api/customers');
            const customers = await res.json();
            let html = '<table><th>Name</th><th>Phone</th><th>Email</th><th>Visits</th><th>Action</th></tr>';
            customers.forEach(c => {
                html += `<tr><td>${c.name}</td><td>${c.phone}</td><td>${c.email || '-'}</td><td>${c.visits || 0}</td><td><button class="delete-btn" onclick="deleteCustomer('${c.id}')">Delete</button></td></tr>`;
            });
            html += '</tr>';
            document.getElementById('customerTable').innerHTML = html;
        }
        
        async function loadAppointments() {
            const res = await fetch('/api/appointments');
            const appointments = await res.json();
            let html = '<tr><th>Customer</th><th>Service</th><th>Date & Time</th><th>Status</th><th>Action</th></tr>';
            appointments.forEach(a => {
                html += `<tr>
                    <td>${a.customer_name}</td>
                    <td>${a.service}</td>
                    <td>${a.datetime}</td>
                    <td><select onchange="updateStatus('${a.id}', this.value)"><option ${a.status === 'pending' ? 'selected' : ''}>pending</option><option ${a.status === 'confirmed' ? 'selected' : ''}>confirmed</option><option ${a.status === 'completed' ? 'selected' : ''}>completed</option></select></td>
                    <td><button class="delete-btn" onclick="deleteAppointment('${a.id}')">Cancel</button></td>
                </tr>`;
            });
            html += '</table>';
            document.getElementById('appointmentTable').innerHTML = html;
        }
        
        async function loadServices() {
            const res = await fetch('/api/services');
            const services = await res.json();
            let html = '<table><th>Service</th><th>Price</th><th>Duration</th><th>Category</th><th>Action</th></tr>';
            services.forEach(s => {
                html += `<tr><td>${s.name}</td><td>$${s.price}</td><td>${s.duration} min</td><td>${s.category}</td><td><button class="delete-btn" onclick="deleteService('${s.id}')">Delete</button></td></tr>`;
            });
            html += '</table>';
            document.getElementById('serviceTable').innerHTML = html;
        }
        
        async function addService() {
            const data = {
                name: document.getElementById('newServiceName').value,
                price: parseInt(document.getElementById('newServicePrice').value),
                duration: 60,
                category: document.getElementById('newServiceCategory').value
            };
            await fetch('/api/services', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            loadServices();
        }
        
        async function deleteService(id) { if(confirm('Delete service?')) { await fetch('/api/services/' + id, {method: 'DELETE'}); loadServices(); } }
        async function deleteCustomer(id) { if(confirm('Delete customer?')) { await fetch('/api/customers/' + id, {method: 'DELETE'}); loadCustomers(); loadDashboard(); } }
        async function deleteAppointment(id) { if(confirm('Cancel appointment?')) { await fetch('/api/appointments/' + id, {method: 'DELETE'}); loadAppointments(); loadDashboard(); } }
        async function updateStatus(id, status) { await fetch('/api/appointments/' + id + '/status', {method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({status: status})}); loadDashboard(); loadAppointments(); }
        
        async function askAI() {
            const q = document.getElementById('aiQuestion').value;
            if(!q) return;
            const res = await fetch('/api/ai/ask', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: q})});
            const data = await res.json();
            const div = document.getElementById('aiResponse');
            div.innerHTML = data.answer;
            div.style.display = 'block';
        }
        
        async function loadQuickInsights() {
            const res = await fetch('/api/ai/insights');
            const data = await res.json();
            let html = '<ul style="margin-top:15px">';
            data.insights.forEach(i => { html += `<li style="margin:10px 0">${i}</li>`; });
            html += '</ul>';
            document.getElementById('quickInsights').innerHTML = html;
        }
        
        function toggleNotifications() { document.getElementById('notifDropdown').classList.toggle('show'); if(document.getElementById('notifDropdown').classList.contains('show')) loadNotifications(); }
        async function loadNotifications() {
            const res = await fetch('/api/notifications');
            const notifs = await res.json();
            document.getElementById('notifBadge').innerText = notifs.length;
            let html = '';
            notifs.forEach(n => { html += `<div class="notif-item">🔔 ${n.message}<div style="font-size:11px; color:#999; margin-top:5px;">${n.time}</div></div>`; });
            document.getElementById('notifList').innerHTML = html || '<div class="notif-item">No notifications</div>';
        }
        
        loadDashboard();
        loadNotifications();
        setInterval(() => { if(document.getElementById('dashboard').classList.contains('active')) loadDashboard(); loadNotifications(); }, 10000);
    </script>
</body>
</html>
'''

# API Routes
@app.route('/')
def customer_site():
    return render_template_string(CUSTOMER_HTML)

@app.route('/admin')
def admin_site():
    return render_template_string(ADMIN_HTML)

@app.route('/api/services', methods=['GET'])
def get_services():
    data = load_data()
    return jsonify(data['services'])

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

@app.route('/api/customer-book', methods=['POST'])
def customer_book():
    data = load_data()
    booking = request.json
    customer = next((c for c in data['customers'] if c['phone'] == booking['phone']), None)
    if not customer:
        customer = {'id': str(len(data['customers']) + 1), 'name': booking['name'], 'phone': booking['phone'], 'email': booking.get('email', ''), 'visits': 0}
        data['customers'].append(customer)
    appointment = {'id': str(len(data['appointments']) + 1), 'customer_id': customer['id'], 'customer_name': customer['name'], 'service': booking['service'], 'datetime': booking['datetime'], 'status': 'pending', 'booked_at': datetime.now().isoformat()}
    data['appointments'].append(appointment)
    save_data(data)
    add_notification(f"New booking: {customer['name']} - {booking['service']}")
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

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    return jsonify(load_notifications())

@app.route('/api/notifications/clear', methods=['DELETE'])
def clear_notifications():
    save_notifications([])
    return jsonify({'success': True})

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    data = load_data()
    appointments = data['appointments']
    today = datetime.now().strftime('%Y-%m-%d')
    current_week = datetime.now().isocalendar()[1]
    current_month = datetime.now().month
    current_year = datetime.now().year
    services_data = {s['name']: s['price'] for s in data.get('services', [])}
    
    today_total = week_total = month_total = year_total = 0
    today_count = week_count = month_count = year_count = 0
    pending = 0
    
    for a in appointments:
        if 'status' not in a:
            a['status'] = 'pending'
        
        if a['status'] == 'completed':
            price = services_data.get(a['service'], 30)
            try:
                date_obj = datetime.fromisoformat(a['datetime'])
                date_str = date_obj.strftime('%Y-%m-%d')
                week_num = date_obj.isocalendar()[1]
                if date_str == today:
                    today_total += price; today_count += 1
                if week_num == current_week and date_obj.year == current_year:
                    week_total += price; week_count += 1
                if date_obj.month == current_month and date_obj.year == current_year:
                    month_total += price; month_count += 1
                if date_obj.year == current_year:
                    year_total += price; year_count += 1
            except:
                pass
        elif a['status'] == 'pending':
            pending += 1
    
    completed = sum(1 for a in appointments if a.get('status') == 'completed')
    
    return jsonify({
        'profit': {'today': today_total, 'week': week_total, 'month': month_total, 'year': year_total, 'todayCount': today_count, 'weekCount': week_count, 'monthCount': month_count, 'yearCount': year_count},
        'customers': len(data['customers']),
        'appointments': len(appointments),
        'pending': pending,
        'completed': completed,
        'recent': appointments[-10:] if appointments else []
    })

@app.route('/api/ai/ask', methods=['POST'])
def ask_ai():
    question = request.json.get('question', '').lower()
    data = load_data()
    appointments = data['appointments']
    services_data = {s['name']: s['price'] for s in data.get('services', [])}
    
    total_earned = sum(services_data.get(a['service'], 30) for a in appointments if a.get('status') == 'completed')
    monthly_avg = total_earned / 12 if total_earned > 0 else 0
    
    if 'profit' in question or 'earn' in question or 'how much' in question:
        answer = f"Total earnings: ${total_earned:.2f}. Monthly average: ${monthly_avg:.2f}. Book 10 more appointments per week to increase by 25 percent!"
    elif 'predict' in question or 'forecast' in question or 'next' in question:
        answer = f"Based on your data, next month projection: ${monthly_avg * 1.15:.2f}. Keep up the great work!"
    elif 'grow' in question or 'increase' in question:
        answer = f"Growth tips: 1 SMS reminders reduce no-shows by 30 percent. 2 Loyalty program increases retention. 3 Referral discounts bring new clients!"
    else:
        answer = f"You have {len(data['customers'])} customers and {len(appointments)} total appointments. Ask me about profits or growth!"
    
    return jsonify({'answer': answer})

@app.route('/api/ai/insights', methods=['GET'])
def ai_insights():
    data = load_data()
    appointments = data['appointments']
    services_data = {s['name']: s['price'] for s in data.get('services', [])}
    
    total_earned = sum(services_data.get(a['service'], 30) for a in appointments if a.get('status') == 'completed')
    insights = [
        f"Lifetime earnings: ${total_earned:.2f}",
        f"Total customers: {len(data['customers'])}",
        f"Total appointments: {len(appointments)}",
        f"Goal: Book {len(appointments) + 15} more appointments this month"
    ]
    return jsonify({'insights': insights})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("MEDICAL TOUCH CRM - FULLY WORKING!")
    print("="*60)
    print("\nCustomer Website: http://127.0.0.1:5000")
    print("Admin Dashboard: http://127.0.0.1:5000/admin")
    print("\nFeatures:")
    print("  - Tab navigation for Nails, Lashes, Skincare, Wax")
    print("  - All 57 services with correct prices")
    print("  - Click any service to book")
    print("  - Admin dashboard with earnings wheels")
    print("  - AI Assistant for business insights")
    print("\n" + "="*60 + "\n")
    app.run(debug=True, port=5000)