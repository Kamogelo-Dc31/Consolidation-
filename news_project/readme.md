# 📰 Django News Publishing Platform

This project is a Django-based news publishing platform with custom user roles (Reader, Editor, Journalist), article approval workflow, RESTful API access, and MariaDB backend.

---
# 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/news_project.git
cd news_project

### 2. Create and Activate a Virtual Environment
    python -m venv venv
    venv\Scripts\activate

### 3. Install Dependencies
    pip install -r requirements.txt

### 4. Configure the Databas
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mariadb_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

### 5. Run database migrations
    python manage.py makemigrations
    python manage.py migrate

### 6. Create a superuser (admin login)
    python manage.py createsuperuser

### 7. Run the development server
    python manage.py runserver

## 🚀 Features

- Custom user model with roles and permissions:
  - Reader: can view articles and newsletters.
  - Editor: can review, approve, update, or delete content.
  - Journalist: can create and manage their own articles and newsletters.
- Editor approval system for articles.
- Signals to:
  - Email subscribed Readers.
  - Post article updates to X (Twitter) via API.
- REST API to expose articles based on Reader subscriptions.
- Fully unit tested with Django and DRF.
- Uses **MariaDB** as the database backend.

---

