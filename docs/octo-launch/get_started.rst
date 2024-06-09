Get Started
-----------

- You can Just run dev-docker to start development mode

.. code-block:: bash

    just dev-docker up

- An .env file will be created by default and configured to work with dev-docker. If you created a previous .env file, it will not be created by default. You can look at .env.template to understand the required configurations and .env.dev to know the default configuration of the dev-docker container.

- Whenever the system starts, the first user will be created as an administrator, and their data will be generated inside the .envs/.admin file. During the development stage, you can set the admin account data to be static, or you can leave it empty to be generated randomly. In the production stage, a random password will be generated mandatorily. Please do not keep the file or change the password during production, or follow your own security method.

.. code-block:: env

    # .envs/.admin
    email='admin@email.com'
    password='your-password'
