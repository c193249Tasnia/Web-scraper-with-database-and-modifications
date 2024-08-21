import os
from mysql.connector import Error
from data_connection import create_data_connection

def execute_query(connection, query, data=None):
    with connection.cursor() as cursor:
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            connection.commit()
            print("Query successful")
        except Error as e:
            print(f"Error executing query: {e}")

def fetch_single_result(connection, query, data):
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        result = cursor.fetchone()
    return result[0] if result else None

def insert_category(connection, name, description):
    query = """
    INSERT INTO categories (name, description)
    VALUES (%s, %s)
    """
    data = (name, description)
    execute_query(connection, query, data)

def get_category_id(connection, category_name):
    query = "SELECT id FROM categories WHERE name = %s"
    return fetch_single_result(connection, query, (category_name,))

def insert_reporter(connection, name, email):
    query = """
    INSERT INTO reporters (name, email)
    VALUES (%s, %s)
    """
    data = (name, email)
    execute_query(connection, query, data)

def get_reporter_id(connection, reporter_name):
    query = "SELECT id FROM reporters WHERE name = %s"
    return fetch_single_result(connection, query, (reporter_name,))

def insert_publisher(connection, name, email):
    query = """
    INSERT INTO publishers (name, email)
    VALUES (%s, %s)
    """
    data = (name, email)
    execute_query(connection, query, data)

def get_publisher_id(connection, publisher_name):
    query = "SELECT id FROM publishers WHERE name = %s"
    return fetch_single_result(connection, query, (publisher_name,))

def insert_news(connection, category_id, reporter_id, publisher_id, news_datetime, title, body, link):
    query = """
    INSERT INTO news (category_id, reporter_id, publisher_id, datetime, title, body, link)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data = (category_id, reporter_id, publisher_id, news_datetime, title, body, link)
    execute_query(connection, query, data)

def get_news_id(connection, title):
    query = "SELECT id FROM news WHERE title = %s"
    return fetch_single_result(connection, query, (title,))

def insert_image(connection, news_id, image_url):
    query = """
    INSERT INTO images (news_id, image_url)
    VALUES (%s, %s)
    """
    data = (news_id, image_url)
    execute_query(connection, query, data)

def insert_summary(connection, news_id, summary_text):
    query = """
    INSERT INTO summaries (news_id, summary_text)
    VALUES (%s, %s)
    """
    data = (news_id, summary_text)
    execute_query(connection, query, data)

if __name__ == "__main__":
    conn = create_data_connection()
    if conn:
        # Example usage:
        # insert_category(conn, "Technology", "News related to technology")
        pass
