import sys
import django
import os
from config.utils.general import get_settings_module


class Manager:
    """The Manager class is responsible for modifying or adding some features in the manage.py file in Django.

    Attributes:
        _schema (dict): A dictionary defining the available commands
            that can be executed from the manage.py file.
        _hook (dict): A dictionary defining hooks that can be executed
            before running the main commands.
        _args (list): The command-line arguments passed to the script.
        error (bool): A flag indicating whether to raise errors or exit silently.
        use_django (bool): A flag indicating whether to set up the Django environment.

    Methods:
        __init__: Initializes the Manager object and stores the command-line arguments provided.
        validate: Validates the input parameters and ensures that the required conditions are met.
        validate_file: Ensures the script is being run from manage.py.
        validate_schema: Ensures the schema attribute is a dictionary.
        set_schema: Adds new commands to the schema.
        set_hook: Adds new hooks to the hook dictionary.
        setup: Sets up the Django environment by configuring the settings module and initializing Django.
        run_hook: Executes any hooks that match the command-line arguments.
        run: Executes the specified command based on the provided arguments.
        no_error: Sets the error flag to False to prevent raising errors.
        no_django: Sets the use_django flag to False to skip Django setup.

    Usage:
        You can execute this object and add its features to a new object upon execution.
        This allows you to enhance the new object with the capabilities of the original one.
        All validate_ processes will be executed during this process.
        Therefore, it's crucial to ensure accurate configuration.
        The functions are executed via the schema file.
        You must correctly specify the command name and function name
        to ensure that any desired command can be executed and its features added to the new object.
    """

    _schema = {}
    _hook = {
        "--no-error": "no_error",
        "--no-django": "no_django",
    }

    def __init__(self) -> None:
        self._args = sys.argv
        self.error = True
        self.use_django = True
        self.django_run = False

    def validate(self) -> None:
        """Validates all the necessary conditions by executing methods starting with 'validate_'."""
        members = dir(self)
        for member in members:
            if member.startswith("validate_"):
                validate_function = getattr(self, member)
                validate_function()

    def validate_file(self) -> None:
        """Ensures that this script is being executed from manage.py file."""
        if "manage.py" not in self._args[0]:
            raise ValueError("You can only use this on the manage.py file")

    def validate_schema(self) -> None:
        """Validates that the _schema attribute is a dictionary."""
        if not isinstance(self._schema, dict):
            raise ValueError("Invalid _schema format. Expected a dictionary.")

    def set_schema(self, new_schema: dict) -> None:
        """Adds new commands to the schema after checking for duplicates.

        Args:
            new_schema (dict): A dictionary of new commands to add to the schema.

        Raises:
            ValueError: If a duplicate key is found in the schema.
        """
        for items in new_schema.items():
            itemA, itemB = items
            if self._schema.get(itemA):
                raise ValueError(
                    f"Duplicate key found: {itemA} in schema."
                    + " Please ensure unique keys."
                )
        self._schema = {**self._schema, **new_schema}

    def set_hook(self, new_hook: dict) -> None:
        """Adds new hooks to the hook dictionary after checking for duplicates.

        Args:
            new_hook (dict): A dictionary of new hooks to add to the hook dictionary.

        Raises:
            ValueError: If a duplicate key is found in the hook dictionary.
        """
        for items in new_hook.items():
            itemA, itemB = items
            if self._hook.get(itemA):
                raise ValueError(
                    f"Duplicate key found: {itemA} in hook."
                    + " Please ensure unique keys."
                )

        self._hook = {**self._hook, **new_hook}

    def setup(self) -> None:
        """Sets up the Django environment by validating conditions, running hooks, and initializing Django."""
        self.validate()
        self.run_hook()
        self.run()

    def django_setup(self):
        if self.use_django:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())
            django.setup()
            self.django_run = True

    def run_hook(self) -> None:
        """Executes any hooks that match the command-line arguments."""
        if len(self._args) > 1:
            for arg in self._args:
                if "--" not in arg[:2]:
                    continue
                method_name = self._hook.get(arg, None)
                if method_name:
                    method = getattr(self, method_name)
                    method()

    def run(self) -> None:
        """Executes the specified command based on the provided arguments.

        Raises:
            ValueError: If no valid command is provided.
        """
        is_use = True
        if len(self._args) > 1:
            for arg in self._args:
                if arg[:2] in ["--", "manage.py"]:
                    continue
                try:
                    method_name = self._schema.get(arg, None)
                    if method_name:
                        is_use = False
                        method = getattr(self, method_name)
                        if not self.django_run:
                            self.django_setup()
                        method()
                except ValueError as e:
                    if self.error:
                        raise ValueError(str(e))
                    exit(0)

            if is_use:
                raise ValueError("foo")
        raise ValueError("foo")

    def no_error(self) -> None:
        """Sets the error flag to False to prevent raising errors."""
        self.error = False
        sys.argv.remove("--no-error")

    def no_django(self) -> None:
        """Sets the use_django flag to False to skip Django setup."""
        self.use_django = False
        sys.argv.remove("--no-django")
