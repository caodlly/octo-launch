@start: stop
    chmod +x ./scripts/start
    ./scripts/start

@stop:
    chmod +x ./scripts/stop
    ./scripts/stop

@restart: stop start

@install:
    pip install uv
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


test path='apps':
    pytest -n auto {{path}}

@cicd-test:
    pytest -n auto

@check_database:
    python manage.py check_database --no-django
    
@createsuperuser:
    python manage.py createsuperuser

@create-admin-pass:
    # Do not use this in production
    python manage.py createsuperuser > ADMIN_PASS
    cat ADMIN_PASS

@collectstatic:
    python manage.py collectstatic --noinput

@search-files query="#LATER" file="*.py":
    find . -name "{{file}}" -not -path "*/env/*" -exec grep -nH "{{query}}" {} \;
