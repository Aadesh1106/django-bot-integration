# Django Internship Assignment Project

## Overview
This project demonstrates Django REST Framework, authentication, Celery with Redis, and Telegram bot integration. It is designed to fulfill the requirements of the Django Internship Assignment.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env` and fill in your secrets (see below).

---

## Environment Variables Used

Set these in your `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

---

## How to Run Locally

1. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
3. **Start Django server:**
   ```bash
   python manage.py runserver
   ```
4. **Start Redis server:**
   - Make sure Redis is running (see https://redis.io/download)
5. **Start Celery worker:**
   ```bash
   celery -A django_project worker --loglevel=info
   ```
6. **Start Telegram bot:**
   ```bash
   python -m bot.telegram_bot
   ```

---

## API Documentation

### Authentication
- Token and JWT authentication supported.

### Endpoints
- `GET /api/public/` — Public endpoint, no auth required.
- `GET /api/protected/` — Protected endpoint, requires authentication.
- `POST /api/register/` — Register a new user.
- `POST /api/login/` — Login and get tokens.
- `POST /api/token/` — Get JWT token.
- `POST /api/token/refresh/` — Refresh JWT token.
- `GET/POST /api/posts/` — List or create posts (auth required).
- `GET/PUT/DELETE /api/posts/<id>/` — Retrieve, update, or delete a post (auth required).

### Telegram Bot
- Start the bot and send `/start` to register your Telegram username with the backend.

---

## Notes
- All secrets and credentials must be set in `.env`.
- For production, set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- See code comments for further documentation.

---

