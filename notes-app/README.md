# Django Notes App

A small notes app: create / edit / delete / search / pin notes. Built to be containerized.

**Stack:** Django 6.1 · Gunicorn · WhiteNoise (static files) · SQLite by default, PostgreSQL via env vars.

## Project layout
```
notes-app/
├── manage.py
├── requirements.txt
├── .env.example
├── notesproject/        # settings, urls, wsgi
├── notes/               # app: models, views, forms, urls, templates, tests, migrations
├── templates/base.html
└── static/css/style.css
```

## Run locally (no Docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver            # http://localhost:8000
python manage.py test                 # run tests
python manage.py createsuperuser      # optional, for /admin
```

## Endpoints
| Path | Purpose |
|---|---|
| `/` | List + search (`?q=`) |
| `/notes/new/` | Create |
| `/notes/<id>/`, `/edit/`, `/delete/`, `/pin/` | View / edit / delete / toggle pin |
| `/health/` | JSON health check incl. DB ping (200 ok / 503 error) — use for `HEALTHCHECK` |
| `/admin/` | Django admin |

## Environment variables
| Var | Default | Notes |
|---|---|---|
| `DJANGO_SECRET_KEY` | dev key | **Set in prod** |
| `DJANGO_DEBUG` | `True` | Set `False` in container |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | comma-separated; add `0.0.0.0` / your domain |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | – | e.g. `http://localhost:8000` (needed for form POSTs when DEBUG=False behind a proxy/other port) |
| `DJANGO_TIME_ZONE` | `UTC` | e.g. `Asia/Kolkata` |
| `LOG_LEVEL` | `INFO` | logs go to stdout |
| `SQLITE_PATH` | `./db.sqlite3` | point at a volume, e.g. `/app/data/db.sqlite3` |
| `POSTGRES_DB` | – | if set, switches to PostgreSQL |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_HOST` / `POSTGRES_PORT` | `postgres` / – / `db` / `5432` | |

## Containerization hints (your exercise)
- Production command: `gunicorn notesproject.wsgi:application --bind 0.0.0.0:8000 --workers 3`
- Run `python manage.py collectstatic --noinput` at **build** time with `DJANGO_DEBUG=False`
  (WhiteNoise serves the hashed files — no nginx needed).
- Run `python manage.py migrate --noinput` at **start** time (entrypoint), not build time — the DB isn't there during build.
- SQLite: mount a volume and set `SQLITE_PATH` there, or data dies with the container.
- Postgres: add a `db` service in compose, set the `POSTGRES_*` vars; wait for the DB to be healthy before migrating
  (`depends_on: condition: service_healthy`).
- `psycopg[binary]` ships its own libpq, so `python:3.13-slim` needs no extra apt packages.
- Good extras to practice: multi-stage build, non-root user, `.dockerignore`, `HEALTHCHECK` on `/health/`.
