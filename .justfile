# Build the project to run
@build: migrate create-admin-no-error

# Creates django applications
@startapp app_name:
    cd apps && django-admin startapp {{app_name}} --template=../config/utils/app_template

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
    chmod +x scripts/stop-pid
    scripts/stop-pid "server-gunicorn"

# Restart Gunicorn server
@restart-gunicorn: stop-gunicorn start-gunicorn

# Start uwsgi server
@start-uwsgi:
    #!/bin/bash
    set -o errexit
    set -o pipefail
    set -o nounset
    export DEBUG=False
    uwsgi --ini uwsgi.ini

# Stop uwsgi server
@stop-uwsgi:
    uwsgi --stop server-uwsgi.pid

# Restart uwsgi server
@restart-uwsgi:
    uwsgi --reload server-uwsgi.pid

# Install required packages
@install:
    pip install uv
    uv pip install -r requirements/requirements.txt

# Start Django development server
@manage-start:
    python manage.py runserver_plus 0.0.0.0:8080

# Open Django shell
@shell:
    python manage.py shell_plus

# Clean development environment (Do not use in production)
[macos]
[linux]
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
[macos]
[linux]
@celery-worker:
    chmod +x scripts/start-celery-worker
    ./scripts/start-celery-worker

# Start Celery Flower monitoring tool
[macos]
[linux]
@celery-flower:
    chmod +x scripts/start-celery-flower
    ./scripts/start-celery-flower

# Start Celery Beat scheduler
[macos]
[linux]
@celery-beat:
    chmod +x scripts/start-celery-beat
    ./scripts/start-celery-beat


# Create file .env for dev-docker
[macos]
[linux]
@create-dev-env:
    chmod +x scripts/create-dev-env
    ./scripts/create-dev-env

# Manage Docker development environment
@dev-docker *cmd: create-dev-env
    docker compose -f docker-compose.dev.yml {{cmd}}

# Clean Docker dev
@clean-dev-docker:
    docker compose -f docker-compose.dev.yml down
    rm -rf /mnt/django_dev

# Manage Docker docs environment
@docs-docker *cmd: create-dev-env
    docker compose -f docker-compose.docs.yml {{cmd}}

# Manage Docker production uwsgi environment
@uwsgi-docker *cmd:
    docker compose -f docker-compose.uwsgi.yml {{cmd}}

# Manage Docker production gunicorn environment
@gunicorn-docker *cmd:
    docker compose -f docker-compose.gunicorn.yml {{cmd}}
