import sys
import django
import os
from config.utils.general import get_settings_module


class Manager:
    """The Manager class is responsible for modifying or adding some features in the manager.py file in Django.

    Attributes:
        schema (dict): A dictionary defining the available commands
        that can be executed from the manage.py file.

    Methods:
        __init__: Initializes the Manager object and stores the command-line arguments provided.
        validate: Validates the input parameters and ensures that the required conditions are met.
        setup: Sets up the Django environment by configuring the settings module and initializing Django.
        run: Executes the specified command based on the provided arguments.

    How Use:
        "You can execute this object and add its features to a new object upon execution.
        This allows you to enhance the new object with the capabilities of the original one.
        All validate_ processes will be executed during this process.
        Therefore, it's crucial to ensure accurate configuration.
        The functions are executed via the schema file.
        You must correctly specify the command name and function name
        to ensure that any desired command can be executed and its features added to the new object."
    """

    # _schema = {"command_name", "method_name"}
    # use set_schema for add on this
    _schema = {}

    def __init__(self) -> None:
        self._args = sys.argv

    def validate(self) -> None:
        members = dir(self)
        for member in members:
            if member.startswith("validate_"):
                validate_function = getattr(self, member)
                validate_function()

    def validate_file(self) -> None:
        if "manage.py" not in self._args[0]:
            raise ValueError("You can only use this on the manage.py file")

    def validate_schema(self) -> None:
        if not isinstance(self._schema, dict):
            raise ValueError("Invalid _schema format. Expected a dictionary.")
        if len(self._args) > 1 and self._args[1] not in self._schema:
            raise ValueError("foo")

    def set_schema(self, new_schema: dict) -> None:
        """It is used to add a function to the diagram and its existence is checked
        beforehand to prevent overlapping of objects"""

        for items in new_schema.items():
            itemA, itemB = items
            if self._schema.get(itemA):
                raise ValueError(
                    f"Duplicate key found: {itemA} in schema."
                    + " Please ensure unique keys."
                )

        self._schema = {**self._schema, **new_schema}

    def setup(self) -> None:
        self.validate()
        if "--no-django" not in self._args:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())
            django.setup()
        self.run()

    def run(self) -> None:
        if len(self._args) > 1:
            name_method = self._schema.get(self._args[1])
            method = getattr(self, name_method)
            method()
