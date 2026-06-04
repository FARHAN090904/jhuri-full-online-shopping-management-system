# Jhuri - Full Online Shopping Management System

⚠️ **EDUCATIONAL PROJECT - NOT FOR COMMERCIAL USE**

**Copyright © 2026 Md. Farhan Alam. All Rights Reserved.**

[![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red.svg)](LICENSE)
[![DBMS Project](https://img.shields.io/badge/Project-DBMS-blue.svg)]()

---

## 📜 Important Notice

This is an **academic DBMS project** created for educational purposes.

### ✅ You CAN:
- 👀 View and study the code
- 📚 Learn database design and Django implementation
- 🎓 Reference for your own academic projects (with attribution)

### ❌ You CANNOT:
- 💰 Use for commercial purposes
- 📋 Copy and claim as your own
- 🎓 Submit as your academic project (plagiarism)
- 🔄 Redistribute without permission

**For licensing inquiries:** alamfarhan2004@gmail.com

---

## 🔒 Security Notice

⚠️ **Important:** For security reasons, the following files are **NOT** included:
- `settings.py` (contains SECRET_KEY and database credentials)
- `.env` files
- Database dumps with sensitive data

If you want to run this project, you must create your own configuration files.

---

## 🛠️ Tech Stack

**Backend:**
- Django (Python Web Framework)
- MySQL (Database)

**Frontend:**
- HTML5
- CSS3
- JavaScript

## ⚙️ How to Run

Follow these steps carefully to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed before you begin:
- Python 3.10+
- MySQL Server


---
### Step 1 — Clone the Repository

```bash
git clone https://github.com/farhanalam/jhuri-full-online-shopping-management-system.git
cd jhuri-full-online-shopping-management-system
```
---

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**
```bash
  venv\Scripts\activate
```


---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Set Up the MySQL Database

Open your MySQL client and run:

```sql
CREATE DATABASE jhuri_db;
```

---

### Step 5 — Create `settings.py`

Since `settings.py` is not included for security reasons, you must create it manually.

Inside the project's main app folder (e.g., `jhuri/settings.py`), create the file and add the following — replacing the placeholder values with your own:

```python
SECRET_KEY = 'your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jhuri_db',
        'USER': 'your-mysql-username',
        'PASSWORD': 'your-mysql-password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```



---

### Step 6 — Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 7 — Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

---

### Step 8 — Run the Development Server

```bash
python manage.py runserver
```

Now open your browser and go to:
- 🌐 App: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 🔧 Admin Panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## ✨ Features

- User Registration & Login
- JWT Authentication
- Password Reset with OTP
- Product Listing & Search
- Shopping Cart
- Order Management
- Invoice PDF Generation
- User Profile Management

---

## 📸 Screenshots
### 🏠 Homepage
![Homepage](homepage.png)
### 🔐 Login Page
![Login](login.png)
### 📝 Register Page
![Register](register.png)
### 🛒 Cart Module
![Cart](cartmodule.png)
### 💳 Checkout
![Checkout](checkout.png)
### Checkout 
![Checkout Step](checkout(step01).png)
### 🎟️ Apply Coupon
![Apply Coupon](applycoupon.png)
### 🧾 Generate Invoice
![Generate Invoice](generate_invoice(step03).png)
### 🧾 Invoice Downloaded
![Invoice](invoice_downloaded_pdf.png)
### 🚫 Stock Out
![Stock Out](stock_out.png)
### 📦 Order History
![Order History](order_history.png)
### 👤 Profile Edit
![Profile Edit](profile_edit.png)
### 🔑 Forgot Password
![Forgot Password](forgotpassword.png)
### 🔢 OTP Verification
![OTP](otp.png)
### 🌐 OTP Web
![OTP Web](otpin%20web.png)
### 🔄 Password Reset
![Password Reset](password_reset.png)
### 🔒 Password Change in Profile
![Password Change](password_change_inprofile.png)
