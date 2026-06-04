# Jhuri - Full Online Shopping Management System

⚠️ **EDUCATIONAL PROJECT - NOT FOR COMMERCIAL USE**
Copyright © 2026 Md. Farhan Alam. All Rights Reserved.

---

## 📜 Important Notice

This is an academic DBMS project created for educational purposes.

✅ **You CAN:**
- 👀 View and study the code
- 📚 Learn database design and Django implementation
- 🎓 Reference for your own academic projects (with attribution)

❌ **You CANNOT:**
- 💰 Use for commercial purposes
- 📋 Copy and claim as your own
- 🎓 Submit as your academic project (plagiarism)
- 🔄 Redistribute without permission

For licensing inquiries: alamfarhan2004@gmail.com

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

---

## ⚙️ How to Run

Follow these steps carefully to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed before you begin:
- Python 3.10+
- MySQL Server
- Git

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/jhuri.git
cd jhuri
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
- **macOS/Linux:**
```bash
  source venv/bin/activate
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

> 💡 To generate a secret key, run this in your terminal:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

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

🏠 Homepage

🔐 Login Page

📝 Register Page

🛒 Cart Module

💳 Checkout

🎟️ Apply Coupon

🧾 Generate Invoice

🧾 Invoice Downloaded

🚫 Stock Out

📦 Order History

👤 Profile Edit

🔑 Forgot Password

🔢 OTP Verification

🌐 OTP Web

🔄 Password Reset

🔒 Password Change in Profile
