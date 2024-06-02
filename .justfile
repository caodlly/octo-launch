@build: migrate compilemessages create-admin-no-error

@start-gunicorn:
    #!/bin/bash
    set -o errexit
    set -o pipefail
    set -o nounset
    export DEBUG=False
    gunicorn -c gunicorn_config.py

@stop-gunicorn:
    scripts/stop-pid "server-gunicorn"

@restart-gunicorn: stop-gunicorn start-gunicorn

@install:
    uv pip install -r requirements/requirements.txt

@manage-start:
    python manage.py runserver_plus 0.0.0.0:8080

@shell:
    python manage.py shell_plus

[linux, macos]
@clean:
    # Do not use this in production
    find . -path "./apps/*/migrations/*.py" -not -name "__init__.py" -delete
    python manage.py clean_pyc
    python manage.py reset_db
    python manage.py reset_schema
    python manage.py clear_cache
    

@migrate:
    python manage.py makemigrations
    python manage.py migrate

@makemessages:
    python manage.py makemessages --all --ignore=env

@compilemessages:
    python manage.py compilemessages

@cicd-test:
    pytest -vn auto

@check_database:
    python manage.py check_database --no-django
    
@create-admin:
    python manage.py createsuperuser

@create-admin-no-error:
    python manage.py createsuperuser -no-error

@collectstatic:
    python manage.py collectstatic --noinput

@celery-worker:
    #!/bin/bash
    set -o errexit
    set -o pipefail
    set -o nounset
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO'

@celery-flower:
    #!/bin/bash
    set -o errexit
    set -o nounset
    exec watchfiles --filter python celery.__main__.main \
        --args \
        "-A config.celery_app flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""

@celery-beat:
    #!/bin/bash
    set -o errexit
    set -o nounset
    rm -f './celerybeat.pid'
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'

@dev-docker status="status":
    mkdir -p {docker,docker/postgres,docker/postgres/data,docker/redis,docker/redis/data}
    docker compose -f docker-compose-dev.yml {{status}}