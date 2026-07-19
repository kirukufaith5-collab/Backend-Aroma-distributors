# Fine Aromas - Backend API Engine

This is the Flask RESTful API backend for the Aromas distributors platform. It manages user authentication, inventory calculations, farmer delivery processing, and wholesale client order dispatching.

## 🛠️ Backend Tech Stack

* **Core Framework:** Flask (Python)
* **Database ORM:** Flask-SQLAlchemy (SQLAlchemy)
* **Database Migrations:** Flask-Migrate (Alembic)
* **Security & Authentication:** PyJWT (JSON Web Tokens) & Werkzeug (Password Hashing)
* **Cross-Origin Requests:** Flask-CORS (Allows communication with React frontend)

---

## 🚀 Local Installation & Setup Guide

Make sure you have Python 3 installed on your computer. Follow these steps from inside this `backend/` directory:

### 1. Initialize and Activate Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows Command Prompt)
venv\Scripts\activate.bat
