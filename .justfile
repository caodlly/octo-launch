# Build the project to run
@build: migrate create-admin-no-error
@build-dev: create-admin-no-error

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

# Start Django development server && output in logfile
@manage-start-logfile:
    nohup python manage.py runserver_plus 0.0.0.0:8080 > logs/manage.log 2>&1 & echo $! > dev-server.pid

# stop Django development server
@manage-stop-logfile:
    kill -9 $(lsof -i :8080 | grep LISTEN | awk '{print $2}')
    echo "Stop Server" > "logs/manage.log"

# restart Django development server && output in logfile
@manage-restart-logfile: manage-stop-logfile manage-start-logfile

# Listen to the development log file
@open-devlog:
    tail -f logs/manage.log

# Open Django shell
@shell:
    python manage.py shell_plus

# Clean development environment (Do not use in production)
@clean-project: rest_db rest_cache clean-migrations-cache

# clean Migrations file (Do not use in production)
[macos]
[linux]
@clean-migrations-cache:
    find . -path "./app/*/migrations/*.py" -not -name "__init__.py" -delete
    python manage.py clean_pyc

# rest database (Do not use in production)
@rest_db:
    python manage.py reset_db
    python manage.py reset_schema

# rest cache (Do not use in production)
[confirm('Are you sure you want to clear the cache? [y/n]')]
@rest_cache:
    python manage.py clear_cache

# Make and apply migrations
@migrate:
    python manage.py makemigrations
    python manage.py migrate

# Make message files for translation
@makemessages:
    python manage.py makemessages --all --ignore=env --ignore=docs

# Compile message files for translation
@compilemessages:
    python manage.py compilemessages

# Run tests
@cicd-test:
    pytest -vn auto

# Check database status without Django
@check_database:
    python manage.py check_database

# Create superuser
@create-admin:
    python manage.py createsuperuser

# Create superuser without error
@create-admin-no-error:
    python manage.py createsuperuser --no-error

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

# use uv in docker 
@uv-docker *cmd:
    uv pip install {{cmd}} --python /opt/venv/

# Manage Docker development environment
@dev-docker *cmd: create-dev-env
    docker compose -f docker-compose.dev.yml {{cmd}}

# Manage Docker docs environment
@docs-docker *cmd: create-dev-env
    docker compose -f docker-compose.docs.yml {{cmd}}

# Manage Docker production uwsgi environment
@uwsgi-docker *cmd:
    docker compose -f docker-compose.uwsgi.yml {{cmd}}

# Manage Docker production gunicorn environment
@gunicorn-docker *cmd:
    docker compose -f docker-compose.gunicorn.yml {{cmd}}

# Manage Docker production node environment
@node-docker *cmd:
    docker compose -f docker-compose.node.yml {{cmd}}
