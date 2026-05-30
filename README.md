<div align="center">
<img src="screenshots/homepage_top.png" alt="ঝুড়ি Banner" width="100%"/>
ঝুড়ি
Online Shopping Management System
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-C42D08?style=for-the-badge)
![Course](https://img.shields.io/badge/Course-CSE%20222-1a1410?style=for-the-badge)
![Group](https://img.shields.io/badge/Group-Code__Velvet-C42D08?style=for-the-badge)
![University](https://img.shields.io/badge/PCIU-Dept.%20of%20CSE-1a1410?style=for-the-badge)
![Stack](https://img.shields.io/badge/Django%20%7C%20MySQL%20%7C%20HTML%20%7C%20JS-C42D08?style=for-the-badge)
> A full-featured Bengali-language e-commerce platform built for Bangladeshi consumers —
> with real-time stock tracking, JWT authentication, OTP password reset,
> and automatic PDF invoice generation stored directly in the database.
</div>
---
⚠️ Important Notice
> **EDUCATIONAL PROJECT — NOT FOR COMMERCIAL USE**
> Copyright © 2026 Md. Farhan Alam & Arpita Barua Pew. All Rights Reserved.
✅ You CAN	❌ You CANNOT
👀 View and study the code	💰 Use for commercial purposes
📚 Learn database design & Django	📋 Copy and claim as your own work
🎓 Reference with proper attribution	🎓 Submit as your own academic project
	🔄 Redistribute without permission
📧 Licensing inquiries: alamfarhan2004@gmail.com
---
🔒 Security Notice
> ⚠️ For security reasons, the following files are **NOT included** in this repository:
> - `shopbd/settings.py` — contains `SECRET_KEY` and database credentials
> - `.env` files — contains sensitive environment variables
>
> To run this project, you must create your own `settings.py` configuration file.
---
📋 Project Information
Field	Details
Course	Database Management System Sessional — CSE 222
Submitted To	Ratul Barua, Lecturer, Dept. of CSE, PCIU
Group Name	Code_Velvet
Member 1	Md. Farhan Alam — CSE 032 08217
Member 2	Arpita Barua Pew — CSE 032 08238
Submission Date	19 May 2026
---
📸 Screenshots
🔐 Authentication
Registration	Login
![Registration](screenshots/registration.png)	![Login](screenshots/login.png)

Password Reset	OTP Verification
![Reset](screenshots/password_reset.png)	![OTP](screenshots/otp_verification.png)
🏠 Homepage & Products
Homepage	All Products
![Homepage](screenshots/homepage_top.png)	![Products](screenshots/all_products.png)

Search with Price Filter
![Search](screenshots/search_price_filter.png)
👤 Profile Management
Dashboard	Edit Profile	Address
![Dashboard](screenshots/user_dashboard.png)	![Profile](screenshots/edit_profile.png)	![Address](screenshots/address.png)
🛒 Cart & Checkout
Cart	Delivery Address	Payment Method
![Cart](screenshots/cart.png)	![Address](screenshots/checkout_address.png)	![Payment](screenshots/payment_method.png)

Apply Coupon Code
![Coupon](screenshots/coupon_code.png)
📄 Invoice & PDF
Generated Invoice	Downloaded PDF
![Invoice](screenshots/invoice_generated.png)	![PDF](screenshots/invoice_pdf.png)
---
✨ Features
<table>
<tr>
<td width="50%">
🔐 Authentication Module
JWT-based login & registration
OTP password reset (6-digit, 30s timer)
Avatar / profile image upload
Multi-address profile management
Change password from profile
🏠 Product Catalogue
150+ products across 10 categories
Real-time stock bars (60s auto-refresh)
Low stock & out-of-stock badges
Full-text search with debounce
Price sorting: Low → High / High → Low
Category filter pills
🛒 Cart Module
Persistent server-side cart
Live stock validation before adding
Quantity +/− controls
Subtotal + delivery charge calculation
</td>
<td width="50%">
💳 Checkout (3-Step)
Step 1 — Delivery address (saved or new)
Step 2 — Payment method selection
Step 3 — Invoice confirmation
Coupon code support
💰 Payment Methods
Cash on Delivery
Mobile Banking (bKash / Nagad / Rocket)
Credit / Debit Card (Visa, Mastercard)
Bank Transfer
📄 Invoice & PDF System
Auto PDF generation via jsPDF 2.5.1
Stored as base64 in `invoice_pdfs` table
Download anytime from order history
Average size: 6.9 – 7.8 KB per invoice
👤 Profile Management
Inline name & phone edit with save buttons
Avatar upload (base64 stored in DB)
Password change from security tab
Saved delivery addresses
</td>
</tr>
</table>
---
🏗️ System Architecture
```
┌──────────────────────────────────────────────────────┐
│              TIER 1 — Frontend (Browser)             │
│        HTML5  ·  CSS3  ·  Vanilla JS  ·  jsPDF      │
└───────────────────────┬──────────────────────────────┘
                        │
                        │  HTTP / JSON
                        │  Authorization: Bearer <JWT Token>
                        │
┌───────────────────────▼──────────────────────────────┐
│              TIER 2 — Django REST API                │
│      Django 4  ·  DRF  ·  SimpleJWT  ·  CORS        │
│                                                      │
│   accounts · products · cart · orders                │
│   payments · invoices                                │
└───────────────────────┬──────────────────────────────┘
                        │
                        │  Django ORM · mysqlclient
                        │
┌───────────────────────▼──────────────────────────────┐
│              TIER 3 — MySQL Database                 │
│        13 tables  ·  FK constraints  ·  1 view       │
│     invoice_pdfs stores base64 PDF as LONGTEXT       │
└──────────────────────────────────────────────────────┘

  Data Flow:
  User action → JS fetch() → Django view → ORM → MySQL → JSON → DOM update
```
---
🛠️ Tech Stack
Layer	Technology	Purpose
Frontend	HTML5 + CSS3 + Vanilla JS	Single-page application (SPA)
PDF Engine	jsPDF 2.5.1	Client-side invoice generation
Backend	Python + Django 4	REST API & business logic
API Layer	Django REST Framework	Serializers, viewsets, permissions
Authentication	SimpleJWT	JWT token-based auth
Database	MySQL / MariaDB 10.4	Relational data storage
DB GUI	phpMyAdmin (XAMPP)	Database management
Environment	pip + venv	Python dependency management
---
🗄️ Database Schema
```
users           → accounts, roles, password hashes
products        → 150+ products with stock_qty and image_url
categories      → 10 categories with parent-child hierarchy
orders          → placed orders with status and totals
order_items     → price snapshot per item per order
cart            → one cart per user
cart_items      → items inside each cart with quantity
payments        → method (COD/card/mobile/bank) + status
invoices        → invoice number and amount per order
invoice_pdfs    → base64 PDF (LONGTEXT) + filename + size_kb
addresses       → saved delivery addresses per user
coupons         → discount codes: percentage or fixed amount
roles           → admin / seller / customer
```
---
🔌 API Endpoints
Method	Endpoint	Auth	Description
`POST`	`/api/accounts/login/`	✗	Login → returns JWT token
`POST`	`/api/accounts/register/`	✗	Create new account
`GET`	`/api/accounts/profile/`	✓	User profile + saved addresses
`PUT`	`/api/accounts/update-profile/`	✓	Update name / phone
`POST`	`/api/accounts/update-avatar/`	✓	Upload profile picture
`POST`	`/api/accounts/change-password/`	✓	Change password
`POST`	`/api/accounts/add-address/`	✓	Save new delivery address
`POST`	`/api/accounts/send-otp/`	✗	Send OTP for password reset
`GET`	`/api/products/`	✗	Product list (search, filter, sort)
`GET`	`/api/products/categories/`	✗	All categories
`GET`	`/api/products/{id}/`	✗	Single product + current stock
`GET`	`/api/cart/`	✓	Get current cart
`POST`	`/api/cart/`	✓	Add item to cart
`PUT`	`/api/cart/`	✓	Update item quantity
`DELETE`	`/api/cart/`	✓	Remove item from cart
`POST`	`/api/orders/checkout/`	✓	Place order → returns order_id + invoice_id
`GET`	`/api/orders/`	✓	All orders for current user
`GET`	`/api/orders/{id}/`	✓	Order detail with items and address
`POST`	`/api/payments/callback/`	✓	Record payment method
`GET`	`/api/invoices/my-invoices/`	✓	List invoices with has_pdf flag
`POST`	`/api/invoices/upload-pdf/`	✓	Store jsPDF base64 in DB
`GET`	`/api/invoices/{id}/download-pdf/`	✓	Download stored PDF file
Product query parameters:
```
GET /api/products/?search=samsung&category=4&ordering=-price&page=1&page_size=20
```
---
🚀 Setup & Installation
Prerequisites
Python 3.10+
XAMPP running (MySQL on port 3306)
`online_shopping` database imported
---
Step 1 — Import Database
```
Open phpMyAdmin → http://localhost/phpmyadmin
Create database: online_shopping
Click Import → select: database/online_shopping.sql
```
---
Step 2 — Clone & Install
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/jhuri-ecommerce.git
cd jhuri-ecommerce

# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
---
Step 3 — Create settings.py
Since `shopbd/settings.py` is not included for security reasons,
create it yourself with your database credentials:
```python
# shopbd/settings.py

SECRET_KEY = 'your-secret-key-here'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'online_shopping',
        'USER': 'root',
        'PASSWORD': '',        # your XAMPP MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
---
Step 4 — Run Server
```bash
python manage.py runserver 8000
```
API running at: http://127.0.0.1:8000
---
Step 5 — Open Frontend
```
Open index.html using VS Code Live Server
```
> ⚠️ Do NOT double-click index.html — use Live Server to avoid CORS errors
---
🔑 Demo Credentials
Email	Password	Role
`karim@shop.com`	`password123`	Customer
`sumaiya@shop.com`	`password123`	Customer
`rahim@shop.com`	`password123`	Seller
---
📁 Project Structure
```
jhuri-ecommerce/
│
├── 📄 index.html              ← Complete frontend (SPA)
├── 📄 manage.py               ← Django entry point
├── 📄 requirements.txt        ← Python dependencies
├── 📄 run_server.bat          ← Windows quick-start
├── 📄 README.md               ← This file
│
├── 📁 accounts/               ← Login, register, OTP, profile, avatar
├── 📁 products/               ← Catalogue, categories, stock
├── 📁 cart/                   ← Cart management
├── 📁 orders/                 ← Checkout, order history
├── 📁 payments/               ← Payment method recording
├── 📁 invoices/               ← PDF upload & download
├── 📁 backend/                ← Django config
│
├── 📁 database/
│   └── 📄 online_shopping.sql ← Full MySQL dump (13 tables)
│
└── 📁 screenshots/            ← All project screenshots
    ├── homepage_top.png
    ├── all_products.png
    ├── registration.png
    ├── login.png
    └── ... (17 screenshots total)
```
---
🐛 Troubleshooting
`mysqlclient` install fails on Windows?
```bash
pip install PyMySQL
```
Add to `shopbd/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```
CORS errors in browser?
Open `index.html` via VS Code Live Server — not by double-clicking
Backend already has `CORS_ALLOW_ALL_ORIGINS = True`
"Table doesn't exist" error?
```
phpMyAdmin → Import → select online_shopping.sql
```
---
🔮 Future Development
[ ] Real bKash Merchant & Nagad payment API integration
[ ] Seller dashboard for product & inventory management
[ ] Order tracking with SMS / email notifications
[ ] Product review and rating system
[ ] React frontend migration for better state management
---
👥 Team — Code_Velvet
Name	Student ID
Md. Farhan Alam	CSE 032 08217
Arpita Barua Pew	CSE 032 08238
Department of Computer Science & Engineering
Port City International University (PCIU)
---
<div align="center">
ঝুড়িতে কেনাকাটার জন্য ধন্যবাদ! 🛒
Made with ❤️ by Code_Velvet — PCIU CSE 032
</div>
