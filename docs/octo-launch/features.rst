Features
========

- **Pre-configured Settings:** Essential settings are already configured, allowing you to focus on developing features rather than setup.
- **Ready-to-Use Commands:** `just <https://github.com/casey/just>`_ commands are provided to streamline project setup and management.
- **Celery and Redis Integration:** `Celery <https://github.com/celery/django-celery>`_ and `Redis <https://github.com/jazzband/django-redis>`_ have been added to the project, providing a suitable development environment for asynchronous task processing and caching.
- **API Development Focus:** The template focuses on developing an API interface, streamlining the creation and management of API endpoints.
- **Mailpit Integration:** `Mailpit <https://mailpit.axllent.org/>`_ has been added for email testing, allowing you to test email functionality easily during development.
- **Storage Configuration:** Pre-configured settings for both local and `S3 <https://aws.amazon.com/ar/pm/serv-s3/>`_ storage options are available, making it easy to switch between different storage backends.
- **Documentation with DRF-Spectacular:** Documentation is built using `DRF-Spectacular <https://drf-spectacular.readthedocs.io/en/latest/>`_, providing a comprehensive and user-friendly way to document your API.
- **Initial Applications:** Two applications, `users` and `accounts`, are pre-configured as starting points. These include basic operations for user creation and management, which can be customized further.
- **Sphinx Documentation Environment:** A `Sphinx <https://www.sphinx-doc.org/>`_ documentation environment is set up and ready to use, making it easy to generate and maintain project documentation.
- **App.json File:** An `config.app.json` file is included to supply application data once and manage it within the project, streamlining application configuration.
- **Docker Environments:** Both development and production environments are configured using `Docker <https://www.docker.com>`_, ensuring consistency across different stages of deployment.
- **Pytest Testing Environment:** A complete `pytest <https://pytest-django.readthedocs.io/en/latest/>`_ testing environment is set up, with pre-configured test files for `users` and `accounts` applications, facilitating thorough testing.
- **Use of `apps` Directory:** The project uses an `apps` directory to organize application files separately. This approach allows you to create new applications in each project without the need to rename the `apps` directory each time.
- **Manager Decorator:** A `manager` decorator is created to add custom commands to the `manage.py` file. Refer to the documentation for guidance on when and how to use this decorator.
- **UWSGI and Gunicorn:** Both `UWSGI <https://uwsgi-docs.readthedocs.io/>`_ and `Gunicorn <https://docs.gunicorn.org/>`_ are provided with basic production settings. It is recommended to fine-tune these settings to match your specific requirements.

These features make it easier to kickstart your development process, allowing you to concentrate on building your application's functionality.

