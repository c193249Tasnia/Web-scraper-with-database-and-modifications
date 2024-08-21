import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def create_data_connection():
    """
    Create a database connection to the MySQL database specified by the environment variables.

    Returns
    -------
    connection : mysql.connector.connection.MySQLConnection or None
        The connection object to the database if successful, None otherwise.
    """
    try:
        # Retrieve environment variables
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASS")
        database = os.getenv("DB_NAME")

        # Ensure all required environment variables are present
        if not all([host, user, passwd, database]):
            raise ValueError("One or more required environment variables are missing.")

        # Establish the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        print("MySQL Database connection successful")
        return connection

    except Error as e:
        print(f"MySQL Error: {e}")
        return None
    except ValueError as ve:
        print(f"Environment Configuration Error: {ve}")
        return None

def close_data_connection(connection):
    """
    Close the database connection.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to be closed.
    """
    if connection.is_connected():
        connection.close()
        print("MySQL Database connection closed")

# Usage example
if __name__ == "__main__":
    conn = create_data_connection()
    if conn:
        # Perform your database operations here
        close_data_connection(conn)
