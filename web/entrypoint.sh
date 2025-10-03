#!/usr/bin/env bash
set -e

# ожидание БД
python - <<'PY'
import time, socket, os
host = os.getenv("PGHOST","db"); port = int(os.getenv("PGPORT","5432"))
for _ in range(60):
    try:
        with socket.create_connection((host, port), 2): break
    except OSError: time.sleep(1)
PY

# миграции и запуск
python manage.py migrate || true
python manage.py collectstatic --noinput || true

exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 60 \
  --graceful-timeout 30