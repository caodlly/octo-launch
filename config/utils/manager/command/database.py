from octo.handler.command import Command


class DBConnect(Command):
    """Verify database connection"""

    def handle(self):
        # === import =====================================
        from django.db import connections
        from django.db.utils import OperationalError
        from colorama import Fore, Style, init
        import time

        init()
        # === Logic ======================================
        connection_attempts = 5
        attempt_interval = 2

        for attempt in range(1, connection_attempts + 1):
            try:
                # Use Django's default database connection
                db_conn = connections["default"]
                c = db_conn.cursor()
                c.execute("SELECT 1")
                c.close()
                print(
                    Fore.GREEN
                    + Style.BRIGHT
                    + "Connected to the database successfully."
                    + Style.RESET_ALL
                )
                exit(0)
            except OperationalError as e:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + f"Attempt {attempt}/{connection_attempts}: Unable to connect to the database: {e}"
                    + Style.RESET_ALL
                )
                time.sleep(attempt_interval)

        print(
            Fore.RED
            + Style.BRIGHT
            + "Failed to connect to the database after multiple attempts."
            + Style.RESET_ALL
        )
        exit(1)
