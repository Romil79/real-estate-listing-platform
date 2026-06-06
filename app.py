# ============================================================
# Real Estate Listing Platform - Pune
# Developer  : Romil Pawar
# Copyright  : © 2026 Romil Pawar. All Rights Reserved.
# ============================================================
from flask import Flask, request, jsonify, session, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import Config
import bcrypt

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
CORS(app)

# ─────────────────────────────────────────
#  TEST ROUTE
# ─────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


# ─────────────────────────────────────────
#  AUTH ROUTES
# ─────────────────────────────────────────

# REGISTER
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    name     = data.get('name')
    email    = data.get('email')
    password = data.get('password')
    role     = data.get('role', 'user')   # user or agent
    phone    = data.get('phone', '')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password, role, phone) VALUES (%s,%s,%s,%s,%s)",
            (name, email, hashed.decode('utf-8'), role, phone)
        )
        mysql.connection.commit()
        return jsonify({'message': 'Registered successfully!'}), 201
    except Exception as e:
        return jsonify({'error': 'Email already exists'}), 409
    finally:
        cur.close()


# LOGIN
@app.route('/api/auth/login', methods=['POST'])
def login():
    data     = request.get_json()
    email    = data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        session['user_id'] = user['id']
        session['role']    = user['role']
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id':    user['id'],
                'name':  user['name'],
                'email': user['email'],
                'role':  user['role']
            }
        })
    return jsonify({'error': 'Invalid email or password'}), 401


# LOGOUT
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})


# ─────────────────────────────────────────
#  PROPERTY ROUTES
# ─────────────────────────────────────────

# GET ALL APPROVED PROPERTIES (with optional filters)
@app.route('/api/properties', methods=['GET'])
def get_properties():
    city           = request.args.get('city', '')
    listing_type   = request.args.get('listing_type', '')
    property_type  = request.args.get('property_type', '')
    min_price      = request.args.get('min_price', 0)
    max_price      = request.args.get('max_price', 999999999)

    query = """SELECT p.*, u.name as owner_name, u.phone as owner_phone
               FROM properties p
               JOIN users u ON p.owner_id = u.id
               WHERE p.status = 'approved'"""
    params = []

    if city:
        query += " AND p.city LIKE %s"
        params.append(f'%{city}%')
    if listing_type:
        query += " AND p.listing_type = %s"
        params.append(listing_type)
    if property_type:
        query += " AND p.property_type = %s"
        params.append(property_type)

    query += " AND p.price BETWEEN %s AND %s"
    params.extend([min_price, max_price])
    query += " ORDER BY p.created_at DESC"

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    properties = cur.fetchall()
    cur.close()
    return jsonify(properties)


# GET SINGLE PROPERTY
@app.route('/api/properties/<int:id>', methods=['GET'])
def get_property(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT p.*, u.name as owner_name, u.phone as owner_phone
                   FROM properties p
                   JOIN users u ON p.owner_id = u.id
                   WHERE p.id = %s""", (id,))
    prop = cur.fetchone()
    cur.close()
    if prop:
        return jsonify(prop)
    return jsonify({'error': 'Property not found'}), 404


# ADD PROPERTY
@app.route('/api/properties', methods=['POST'])
def add_property():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO properties
                   (title, description, price, location, city,
                    property_type, listing_type, bhk, area_sqft, image_url, owner_id)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (data['title'], data['description'], data['price'],
                 data['location'], data['city'], data['property_type'],
                 data['listing_type'], data['bhk'], data['area_sqft'],
                 data.get('image_url', ''), data['owner_id']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Property submitted for approval!'}), 201


# DELETE PROPERTY
@app.route('/api/properties/<int:id>', methods=['DELETE'])
def delete_property(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM properties WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Property deleted'})


# ─────────────────────────────────────────
#  INQUIRY ROUTES
# ─────────────────────────────────────────

# SEND INQUIRY
@app.route('/api/inquiries', methods=['POST'])
def send_inquiry():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO inquiries
                   (property_id, sender_name, sender_email, sender_phone, message)
                   VALUES (%s,%s,%s,%s,%s)""",
                (data['property_id'], data['sender_name'],
                 data['sender_email'], data['sender_phone'], data['message']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Inquiry sent successfully!'}), 201


# GET INQUIRIES FOR A PROPERTY
@app.route('/api/inquiries/<int:property_id>', methods=['GET'])
def get_inquiries(property_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inquiries WHERE property_id = %s ORDER BY created_at DESC", (property_id,))
    inquiries = cur.fetchall()
    cur.close()
    return jsonify(inquiries)


# ─────────────────────────────────────────
#  ADMIN ROUTES
# ─────────────────────────────────────────

# GET ALL PENDING PROPERTIES
@app.route('/api/admin/pending', methods=['GET'])
def pending_properties():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM properties WHERE status = 'pending'")
    props = cur.fetchall()
    cur.close()
    return jsonify(props)


# APPROVE OR REJECT PROPERTY
@app.route('/api/admin/approve/<int:id>', methods=['PUT'])
def approve_property(id):
    data   = request.get_json()
    status = data.get('status', 'approved')  # approved or rejected
    cur = mysql.connection.cursor()
    cur.execute("UPDATE properties SET status = %s WHERE id = %s", (status, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': f'Property {status}!'})


# GET ALL USERS
@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role, phone, created_at FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)


# ─────────────────────────────────────────
# ─────────────────────────────────────────
#  PAGE ROUTES (serve HTML pages)
# ─────────────────────────────────────────
from flask import render_template

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/listings')
def listings_page():
    return render_template('listings.html')

@app.route('/property/<int:id>')
def property_detail_page(id):
    return render_template('property_detail.html', property_id=id)

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# GET PROPERTIES BY OWNER
@app.route('/api/properties/my/<int:owner_id>', methods=['GET'])
def get_my_properties(owner_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM properties WHERE owner_id = %s ORDER BY created_at DESC", (owner_id,))
    props = cur.fetchall()
    cur.close()
    return jsonify(props)

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

# ADMIN - GET ALL PROPERTIES
@app.route('/api/admin/all-properties', methods=['GET'])
def all_properties_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM properties ORDER BY created_at DESC")
    props = cur.fetchall()
    cur.close()
    return jsonify(props)

if __name__ == '__main__':
    app.run(debug=True)
# ============================================================
# Real Estate Listing Platform - Pune
# Developer  : Romil Pawar
# Copyright  : © 2026 Romil Pawar. All Rights Reserved.
# ============================================================