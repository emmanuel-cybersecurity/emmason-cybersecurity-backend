# Emmason Cyber Security — FastAPI Backend

Backend API for the Emmason Cyber Security website.

## Features

- FastAPI REST API
- Contact messages
- Service enquiries
- PostgreSQL or SQLite
- Admin JWT authentication
- Pydantic validation
- CORS configuration
- Docker/Railway deployment
- Automatic `/docs` API documentation

## Local setup

Python 3.11+ recommended.

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and change the secrets.

Run:

```bash
uvicorn app.main:app --reload
```

Open:

- `/health`
- `/docs`
- `/redoc`

## API

### Public

`POST /api/contact`

Example:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348000000000",
  "subject": "Security assessment",
  "message": "I would like to discuss a security assessment."
}
```

`POST /api/service-enquiries`

Example:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348000000000",
  "service": "Penetration Testing",
  "details": "I need an assessment of my web application."
}
```

### Admin

Login:

`POST /api/auth/login`

Then send:

`Authorization: Bearer YOUR_TOKEN`

Admin endpoints:

- `GET /api/admin/contacts`
- `GET /api/admin/service-enquiries`
- `PATCH /api/admin/contacts/{message_id}/read`

## Production notes

1. Never commit `.env`.
2. Use a strong random `JWT_SECRET`.
3. Use a strong unique admin password.
4. Restrict `CORS_ORIGINS_RAW` to the actual frontend domain.
5. Use PostgreSQL in production.
6. Put the API behind HTTPS.
7. Add a production rate limiter/reverse proxy before exposing public endpoints.
8. For larger deployments, replace `create_all()` with Alembic migrations.
