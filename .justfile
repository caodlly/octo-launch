start: stop
    chmod +x ./shell/start
    ./shell/start

stop:
    chmod +x ./shell/stop
    ./shell/stop

install:
    python -m pip install --upgrade pip
    uv pip install -r requirements/base.txt
    uv pip install -r requirements/development.txt

docker-start:
    @docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

prod-start:
   @docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

docker-stop:
    @docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

prod-stop:
    @docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

devstart:
    python manage.py runserver 0.0.0.0:8080

[linux]
clean-migrations:
    find . -path "./apps/*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "./apps/*/migrations/*.pyc" -delete

migrate:
    python manage.py makemigrations
    python manage.py migrate

test path='':
    pytest -n auto {{path}}

cicd-test:
    pytest -n auto --disable-warnings

check-database-connection:
    python check_database_connection.py