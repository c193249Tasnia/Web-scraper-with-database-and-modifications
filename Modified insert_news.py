import os
import mysql.connector
from mysql.connector import Error
from db_connection import create_db_connection


def execute_query(connection, query, data=None):
    """Executes a SQL query with optional data and commits the changes."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, data) if data else cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


def insert_category(connection, name, description):
    """Inserts a new category into the categories table."""
    query = """
    INSERT INTO categories (name, description)
    VALUES (%s, %s)
    """
    execute_query(connection, query, (name, description))


def get_category_id(connection, category):
    """Fetches the ID of a category by its name."""
    query = "SELECT id FROM categories WHERE name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (category,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


def insert_reporter(connection, name, email):
    """Inserts a new reporter into the reporters table."""
    query = """
    INSERT INTO reporters (name, email)
    VALUES (%s, %s)
    """
    execute_query(connection, query, (name, email))


def get_reporter_id(connection, reporter):
    """Fetches the ID of a reporter by their name."""
    query = "SELECT id FROM reporters WHERE name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (reporter,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


def insert_publisher(connection, name, email):
    """Inserts a new publisher into the publishers table."""
    query = """
    INSERT INTO publishers (name, email)
    VALUES (%s, %s)
    """
    execute_query(connection, query, (name, email))


def get_publisher_id(connection, publisher):
    """Fetches the ID of a publisher by their name."""
    query = "SELECT id FROM publishers WHERE name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (publisher,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


def insert_news(connection, category_id, reporter_id, publisher_id, datetime, title, body, link):
    """Inserts a news article into the news table."""
    query = """
    INSERT INTO news (category_id, reporter_id, publisher_id, datetime, title, body, link)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(connection, query, (category_id, reporter_id, publisher_id, datetime, title, body, link))


def get_news_id(connection, title):
    """Fetches the ID of a news article by its title."""
    query = "SELECT id FROM news WHERE title = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


def insert_image(connection, news_id, image_url):
    """Inserts an image URL related to a news article."""
    query = """
    INSERT INTO images (news_id, image_url)
    VALUES (%s, %s)
    """
    execute_query(connection, query, (news_id, image_url))


def insert_summary(connection, news_id, summary_text):
    """Inserts a summary related to a news article."""
    query = """
    INSERT INTO summaries (news_id, summary_text)
    VALUES (%s, %s)
    """
    execute_query(connection, query, (news_id, summary_text))


if __name__ == "__main__":
    conn = create_db_connection()
    if conn:
        try:
            # Insert example category
            insert_category(conn, "Politics", "All news related to politics")
            
            # Insert example reporter
            insert_reporter(conn, "John Doe", "john.doe@example.com")
            
            # Insert more data as needed...
        except Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()  # Ensure the connection is closed
