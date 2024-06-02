import psycopg2
from psycopg2 import OperationalError
from config.settings.base import env


def check_database_connection():
    def connect():
        """Verify database connection"""
        try:
            # Get the database configuration URL from environment variables
            db_url = env.db_url("DATABASE_URL")

            # Convert the db_url dictionary to match psycopg2.connect() parameters
            db_config = {
                "dbname": db_url["NAME"],
                "user": db_url["USER"],
                "password": db_url["PASSWORD"],
                "host": db_url["HOST"],
                "port": db_url["PORT"],
            }

            # Connect to the PostgreSQL database
            conn = psycopg2.connect(**db_config)

            # Create a cursor object using the cursor() method
            cursor = conn.cursor()

            # Print PostgreSQL server version
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(
                "\033[32m"
                + f"Connected to PostgreSQL database. PostgreSQL Server version:{db_version}"
                + "\033[0m"
            )

            # Close the cursor and connection
            cursor.close()
            conn.close()
            exit(0)

        except OperationalError as e:
            print(
                "\033[35m"
                + f"Unable to connect to PostgreSQL database: {e}"
                + "\033[0m"
            )

    for i in range(0, 25):
        connect()
        print("\033[31m" + f"Attempt No. {i} out of 25 attempts" + "\033[0m")
    exit(1)
