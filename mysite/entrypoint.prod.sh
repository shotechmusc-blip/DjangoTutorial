#!/bin/sh
set -eu

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_WAIT_SECONDS="${DB_WAIT_SECONDS:-180}"
DB_WAIT_INTERVAL="${DB_WAIT_INTERVAL:-3}"

printf '[entrypoint] Waiting for DB at %s:%s (timeout=%ss)\n' "$DB_HOST" "$DB_PORT" "$DB_WAIT_SECONDS"
python - "$DB_HOST" "$DB_PORT" "$DB_WAIT_SECONDS" "$DB_WAIT_INTERVAL" <<'PY'
import socket
import sys
import time

host = sys.argv[1]
port = int(sys.argv[2])
timeout_seconds = int(sys.argv[3])
retry_interval = float(sys.argv[4])
deadline = time.time() + timeout_seconds
attempt = 0

while time.time() < deadline:
    attempt += 1
    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"[entrypoint] DB reachable on attempt {attempt}")
            sys.exit(0)
    except OSError as exc:
        remaining = max(0, int(deadline - time.time()))
        print(
            f"[entrypoint] DB not reachable yet ({exc}); retry in {retry_interval}s "
            f"(remaining~{remaining}s)"
        )
        time.sleep(retry_interval)

print("[entrypoint] ERROR: DB port did not become reachable in time", file=sys.stderr)
sys.exit(1)
PY

printf '[entrypoint] Running database migrations...\n'
python manage.py migrate

printf '[entrypoint] Collecting static files...\n'
python manage.py collectstatic --noinput

printf '[entrypoint] Starting gunicorn...\n'
exec gunicorn --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-3}" --timeout "${GUNICORN_TIMEOUT:-60}" mysite.wsgi:application
