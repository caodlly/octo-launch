start: stop
    chmod +x ./shell/start
    ./shell/start

stop:
    chmod +x ./shell/stop
    ./shell/stop

install:
    python -m pip install --upgrade pip
    pip install -r requirements.txt

devstart:
    python manage.py runserver 0.0.0.0:8080

[linux]
clean-migrations:
    find . -path "*/migrations/*.py" -not -path "*/env/*" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -not -path "*/env/*" -delete

migrate:
    python manage.py makemigrations
    python manage.py migrate

test path='':
    pytest -n auto {{path}}

cicd-test:
    pytest -n auto --disable-warnings

check-database-connection:
    python check_database_connection.py