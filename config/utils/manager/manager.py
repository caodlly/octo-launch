import sys
from .command import Command


class Manager:
    """The Manager class is responsible for modifying or adding some features in the manage.py file in Django."""

    _schema = {}

    def __init__(self) -> None:
        self._argv = sys.argv

    def validate(self) -> None:
        """Validates all the necessary conditions by executing methods starting with 'validate_'."""
        members = dir(self)
        for member in members:
            if member.startswith("validate_"):
                validate_function = getattr(self, member)
                validate_function()

    def validate_file(self) -> None:
        """Ensures that this script is being executed from manage.py file."""
        if "manage.py" not in self._argv[0]:
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
            if not issubclass(itemB, Command):
                raise ValueError("This class must be an instance of Command")
        self._schema = {**self._schema, **new_schema}

    def setup(self) -> None:
        """Sets up the Django environment by validating conditions, running hooks, and initializing Django."""
        self.validate()
        self.run()

    def help(self):
        from django.core.management import execute_from_command_line
        from colorama import Fore, Style

        execute_from_command_line(self._argv)
        print(Fore.GREEN, Style.BRIGHT, "\n[Manager]", Style.RESET_ALL)
        for command, _class in self._schema.items():
            print(
                "   " + Fore.CYAN,
                command + ":\t",
                Fore.YELLOW,
                _class.__doc__,
                Style.RESET_ALL,
            )
        exit(0)

    def run(self) -> None:
        """Executes the specified command based on the provided arguments.

        Raises:
            ValueError: If no valid command is provided.
        """
        argv = self._argv
        help_fields = ["help", "-h", "--help"]
        if len(argv) > 1:
            if argv[1] in help_fields:
                self.help()
                raise ValueError("foo")

            method = self._schema.get(argv[1], None)

            if method:
                for arg in self._argv:
                    if arg in help_fields:
                        method().help()
                method().setup()
        else:
            self.help()
        raise ValueError("foo")
