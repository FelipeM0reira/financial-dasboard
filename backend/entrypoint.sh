#!/bin/bash
set -e

echo "================================"
echo "Financial Dashboard - Backend"
echo "================================"

# Database configuration
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-budget_tracker}
DB_USER=${DB_USER:-postgres}

echo ""
echo "[1/4] Waiting for PostgreSQL to be ready..."
echo "      Host: $DB_HOST:$DB_PORT"
echo "      Database: $DB_NAME"
echo ""

# Function to check database connectivity
check_db() {
  python -c "
import psycopg2
import sys
try:
    conn = psycopg2.connect(
        host='$DB_HOST',
        port='$DB_PORT',
        database='$DB_NAME',
        user='$DB_USER',
        password='$DB_PASSWORD',
        connect_timeout=5
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f'Connection failed: {e}')
    sys.exit(1)
  "
}

# Retry logic for database connection
RETRY_COUNT=0
MAX_RETRIES=30
RETRY_DELAY=2

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if check_db; then
    echo "✓ PostgreSQL is ready!"
    break
  fi
  
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "  Attempt $RETRY_COUNT/$MAX_RETRIES - waiting ${RETRY_DELAY}s before retry..."
  sleep $RETRY_DELAY
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "✗ ERROR: PostgreSQL did not become available after $((MAX_RETRIES * RETRY_DELAY)) seconds"
  exit 1
fi

echo ""
echo "[2/4] Running database migrations..."
python manage.py migrate --noinput
MIGRATE_EXIT_CODE=$?

if [ $MIGRATE_EXIT_CODE -ne 0 ]; then
  echo "✗ ERROR: Database migrations failed with exit code $MIGRATE_EXIT_CODE"
  exit 1
fi
echo "✓ Database migrations completed successfully"

echo ""
echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "✓ Static files collected"

echo ""
echo "[4/4] Starting Django server..."
echo "================================"
echo ""

exec "$@"
