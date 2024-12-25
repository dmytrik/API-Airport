#!/bin/sh

echo "Waiting for postgres..."
echo $POSTGRES_HOST
echo $POSTGRES_PORT

until python -c "import psycopg2; psycopg2.connect(dbname='$POSTGRES_DB', user='$POSTGRES_USER', password='$POSTGRES_PASSWORD', host='$POSTGRES_HOST', port=$POSTGRES_PORT)"; do
  echo "Waiting for database..."
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate

exec "$@"
