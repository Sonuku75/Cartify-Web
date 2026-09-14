# Cartify Backend Service

This is the core backend API service for the Cartify fashion e-commerce platform. It provides a centralized REST API and PostgreSQL datastore serving the Next.js website, iOS app, and Android app.

---

## Technology Stack

- **Framework**: Python, Django, Django REST Framework
- **Database**: PostgreSQL with connection pooling (`psycopg 3`)
- **Caching & Broker**: Redis
- **Task Worker**: Celery
- **Authentication**: Stateless JWT (`djangorestframework-simplejwt`)

---

## Directory Structure

```
backend/
├── config/             # Project settings, URL routing, Celery, WSGI/ASGI
│   ├── __init__.py     # Exposes Celery app
│   ├── settings.py     # Environment-based configuration
│   ├── urls.py         # Root URL routes (/api/health/, /api/v1/)
│   ├── celery.py       # Celery task manager setup
│   ├── wsgi.py         # WSGI deployment entrypoint
│   └── asgi.py         # ASGI deployment entrypoint
│
├── apps/               # Decoupled domain applications
│   ├── common/         # Cross-cutting utilities, health check, pagination
│   └── ...             # Future domain apps (users, products, orders, etc.)
│
├── manage.py           # Django administrative utility
├── requirements.txt    # Python package dependencies
├── .env.example        # Environment variable template
└── .gitignore          # Backend git exclusion rules
```

---

## Foundation Endpoints

- **Health Check**: `GET /api/health/`
  - Returns `{"status": "ok", "service": "cartify-api"}` with HTTP 200.
- **Versioned API Root**: `/api/v1/`
  - Reserved namespace for future domain endpoints.

---

## Setup & Execution (Reference)

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the local development server:
   ```bash
   python manage.py runserver 8000
   ```
6. Run Celery worker:
   ```bash
   celery -A config worker --loglevel=info
   ```
