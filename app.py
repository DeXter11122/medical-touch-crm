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
            {'id': '22', 'name': 'Full Set Lashes Volume', 'price': 38
