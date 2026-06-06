# 🏠 Real Estate Listing Platform - Pune

A full-stack web-based real estate platform built for the Pune property market.

## 👨‍💻 Developer
- **Name:** Romil Pawar
- **Course:** MCA Management, Semester IV (2024-2026)
- **University:** MIT World Peace University, Pune

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Architecture | REST API |

## ✨ Features
- Property listings for Buy and Rent
- Search and filter by Pune areas
- Agent dashboard to manage listings
- Inquiry system for direct contact
- Admin panel for approvals
- Role-based access (User, Agent, Admin)
- Responsive mobile-friendly design

## 🗺️ Areas Covered in Pune
Baner, Hinjewadi, Kothrud, Wakad, Viman Nagar,
Koregaon Park, Aundh, Hadapsar, Pimple Saudagar, Shivajinagar

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/Romil79/real-estate-listing-platform.git

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install flask flask-mysqldb flask-cors bcrypt python-dotenv

### 4. Create .env file
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=real_estate_db
SECRET_KEY=mysecretkey123

### 5. Setup MySQL Database
- Start XAMPP and run MySQL
- Create database: real_estate_db
- Run the SQL schema to create tables

### 6. Run the application
python app.py

### 7. Open in browser
http://127.0.0.1:5000

## 📄 License
© 2026 Romil Pawar. All Rights Reserved.
