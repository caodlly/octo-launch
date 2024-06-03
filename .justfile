# Build the project to run
@build: migrate compilemessages create-admin-no-error

# Start Gunicorn server
@start-gunicorn:
    #!/bin/bash
    set -o errexit
    set -o pipefail
    set -o nounset
    export DEBUG=False
    gunicorn -c gunicorn_config.py

# Stop Gunicorn server
@stop-gunicorn:
    scripts/stop-pid "server-gunicorn"

# Restart Gunicorn server
@restart-gunicorn: stop-gunicorn start-gunicorn

# Install required packages
@install:
    uv pip install -r requirements/requirements.txt

# Start Django development server
@manage-start:
    python manage.py runserver_plus 0.0.0.0:8080

# Open Django shell
@shell:
    python manage.py shell_plus

# Clean development environment (Do not use in production)
[linux, macos]
@clean:
    find . -path "./apps/*/migrations/*.py" -not -name "__init__.py" -delete
    python manage.py clean_pyc
    python manage.py reset_db
    python manage.py reset_schema
    python manage.py clear_cache

# Make and apply migrations
@migrate:
    python manage.py makemigrations
    python manage.py migrate

# Make message files for translation
@makemessages:
    python manage.py makemessages --all --ignore=env

# Compile message files for translation
@compilemessages:
    python manage.py compilemessages

# Run tests
@cicd-test:
    pytest -vn auto

# Check database status without Django
@check_database:
    python manage.py check_database --no-django

# Create superuser
@create-admin:
    python manage.py createsuperuser

# Create superuser without error
@create-admin-no-error:
    python manage.py createsuperuser -no-error

# Collect static files
@collectstatic:
    python manage.py collectstatic --noinput

# Start Celery worker
@celery-worker:
    #!/bin/bash
    set -o errexit
    set -o pipefail
    set -o nounset
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO'

# Start Celery Flower monitoring tool
@celery-flower:
    #!/bin/bash
    set -o errexit
    set -o nounset
    exec watchfiles --filter python celery.__main__.main --args "-A config.celery_app flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""

# Start Celery Beat scheduler
@celery-beat:
    #!/bin/bash
    set -o errexit
    set -o nounset
    rm -f './celerybeat.pid'
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'

# Manage Docker development environment
@dev-docker *cmd:
    docker compose -f docker-compose.dev.yml {{cmd}}

# Manage Docker docs environment
@docs-docker *cmd:
    docker compose -f docker-compose.docs.yml {{cmd}}
