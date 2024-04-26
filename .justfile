start: stop
    chmod +x ./scripts/start
    ./scripts/start

stop:
    chmod +x ./scripts/stop
    ./scripts/stop

install:
    pip install uv
    uv pip install -r requirements.txt

manage-start:
    python manage.py runserver 0.0.0.0:8080

[linux]
clean-migrations:
    find . -path "./apps/*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "./apps/*/migrations/*.pyc" -delete

migrate:
    python manage.py makemigrations
    python manage.py migrate

translate:
    python manage.py makemessages --all --ignore=env
    python manage.py compilemessages


test path='':
    pytest -n auto {{path}}

cicd-test:
    pytest -n auto --disable-warnings

check_database:
    python manage.py check_database
    
createsuperuser:
    python manage.py createsuperuser