import sys
import os
import django
from config.utils.general import get_settings_module


class Command:
    """Represents a base command class with hooks and setup for Django environment."""

    _hooks = {
        "--no-error": "no_error",
    }

    def __init__(self):
        self._argv = sys.argv
        self.django_run = False  # Determines whether Django is running or not, it is automatically changed when it is running
        self.use_django = True  # Determines whether Django is required or not
        self.debug = True  # It expresses whether error messages will be printed or not, and this can be controlled via a hook called --no-error

    def set_hooks(self, new_hook: dict) -> None:
        """Adds new hooks to the hook dictionary after checking for duplicates.

        Args:
            new_hook (dict): A dictionary of new hooks to add to the hook dictionary.

        Raises:
            ValueError: If a duplicate key is found in the hook dictionary.
        """
        for items in new_hook.items():
            itemA, itemB = items
            if itemA[:2] != "--":
                raise ValueError("The prefix must be '--'")
            if self._hooks.get(itemA):
                raise ValueError(
                    f"Duplicate key found: {itemA} in hook."
                    + " Please ensure unique keys."
                )

        self._hooks = {**self._hooks, **new_hook}

    def help(self) -> None:
        """Prints custom help message for Command class."""
        from colorama import Fore, Style

        for command, hook in self._hooks.items():
            doc = getattr(self, hook).__doc__
            print(Fore.CYAN, command + "\t:", Fore.YELLOW, doc, Style.RESET_ALL)
        exit(0)

    def setup(self) -> None:
        """Sets up the Django environment by validating conditions, running hooks, and initializing Django."""
        self._run_hook()
        self._django_setup()

        try:
            self.handle()
            exit(0)
        except Exception as e:
            if self.debug:
                if str(e) == "foo":
                    """
                    You should not return foo because you should not redirect the command to manager.py.
                    So in this case it will exit suddenly without any error messages
                    """
                    exit(1)
                raise ValueError(str(e))
            exit(1)

    def _run_hook(self) -> None:
        """Executes any hooks that match the command-line arguments."""
        if len(self._argv) > 1:
            for arg in self._argv:
                if "--" not in arg[:2]:
                    continue
                method_name = self._hooks.get(arg, None)
                if method_name:
                    method = getattr(self, method_name)
                    method()

    def _django_setup(self) -> None:
        """Runs the Django environment."""
        if self.use_django:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())
            django.setup()
            self.django_run = True

    def no_error(self) -> None:
        """Prevent returning error."""
        self.debug = False

    def handle(self):
        """Here you create your own command"""
        pass
