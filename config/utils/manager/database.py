import psycopg2
from psycopg2 import OperationalError
from config.settings.base import env


def check_database_connection():
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
            "Connected to PostgreSQL database. PostgreSQL Server version:", db_version
        )

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except OperationalError as e:
        print("Unable to connect to PostgreSQL database:", e)
        exit(1)
