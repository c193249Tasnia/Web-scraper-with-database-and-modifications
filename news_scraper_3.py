import os
import time
from requests_html import HTMLSession
from mysql.connector import Error
from db_connection import create_db_connection
from news_insert_modified import (
    insert_reporter, 
    insert_category, 
    insert_news,
    insert_publisher,
    insert_image
)

# Set environment variable for Pyppeteer
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

def process_and_insert_news_data(connection, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url):
    """
    Processes and inserts news scraping data into the database.

    Parameters
    ----------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    publisher_website : str
        The website of the publisher.
    publisher : str
        The name of the publisher.
    title : str
        The title of the news article.
    reporter : str
        The name of the reporter.
    news_datetime : str
        The publication date and time of the news article.
    category : str
        The category of the news article.
    news_body : str
        The body of the news article.
    images : list of str
        A list of image URLs associated with the news article.
    url : str
        The URL of the news article.
    """
    try:
        # Insert category if not exists
        category_id = insert_category(connection, category, f"{category} af description")
        
        # Insert reporter if not exists
        reporter_id = insert_reporter(connection, reporter, f"{reporter}@hfg.com")
        
        # Insert publisher if not exists
        publisher_id = insert_publisher(connection, publisher, f"{publisher}@ghjey.com")
        
        # Insert news article
        news_id = insert_news(connection, category_id, reporter_id, publisher_id, news_datetime, title, news_body, url)
        
        # Insert images
        for image_url in images:
            insert_image(connection, news_id, image_url)
    
    except Error as e:
        print(f"Error while processing news data - {e}")

def single_news_scraper(url):
    """
    Scrapes a single news article from the provided URL and returns relevant data.

    Parameters
    ----------
    url : str
        The URL of the news article.

    Returns
    -------
    tuple
        A tuple containing publisher_website, publisher, title, reporter, news_datetime, category, news_body, images.
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found
        time.sleep(3)

        publisher_website = url.split('/')[2]       
        publisher = publisher_website.split('.')[-2]  

        # Extract title, reporter, datetime, and category with defaults if not found
        title = response.html.find('h1', first=True).text if response.html.find('h1', first=True) else "No title"
        reporter = response.html.find('.contributor-name', first=True).text if response.html.find('.contributor-name', first=True) else "Unknown"
        datetime_element = response.html.find('time', first=True)
        news_datetime = datetime_element.attrs['datetime'] if datetime_element else "Unknown"
        category = response.html.find('.print-entity-section-wrapper', first=True).text if response.html.find('.print-entity-section-wrapper', first=True) else "Uncategorized"

        # Collect news body paragraphs
        news_body = '\n'.join([p.text for p in response.html.find('p')]) if response.html.find('p') else "No content"

        # Collect image URLs
        img_tags = response.html.find('img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]

        return publisher_website, publisher, title, reporter, news_datetime, category, news_body, images

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def main():
    conn = create_db_connection()
    if conn is not None:
        try:
            url = "https://www.prothomalo.com/bangladesh/k4fpzemipc"
            result = single_news_scraper(url)
            if result:
                publisher_website, publisher, title, reporter, news_datetime, category, news_body, images = result
                process_and_insert_news_data(conn, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url)
            else:
                print(f"Failed to scrape the news article from URL: {url}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
