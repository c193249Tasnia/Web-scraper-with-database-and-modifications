import os
import time
from requests_html import HTMLSession
from mysql.connector import Error
from data_connection import create_data_connection
from insert_news import (
    execute_query,
    insert_reporter,
    get_reporter_id,
    insert_category,
    get_category_id,
    insert_news,
    get_news_id,
    insert_publisher,
    get_publisher_id,
    insert_image
)

# Set environment variable for Pyppeteer
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

def process_and_insert_news_data(connection, publisher_website, publisher, title, reporter, news_datetime, category, news_body, images, url):
    try:
        # Insert category if not exists
        insert_category(connection, category, f"{category} সম্পর্কিত")
        c_id = get_category_id(connection, category)
        
        # Insert reporter if not exists
        insert_reporter(connection, reporter, f"{reporter}@gmail.com")
        r_id = get_reporter_id(connection, reporter)
        
        # Insert publisher if not exists
        insert_publisher(connection, publisher, f"{publisher_website}")
        p_id = get_publisher_id(connection, publisher)
        
        # Insert news article
        news_id = insert_news(connection, c_id, r_id, p_id, news_datetime, title, news_body, url)
        n_id = get_news_id(connection, title)
        
        # Insert images
        for image_url in images:
            insert_image(connection, n_id, image_url)
        
    except Error as e:
        print(f"Error while processing news data: {e}")

def single_news_scraper(url):
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()  # This will download Chromium if not found
        time.sleep(3)

        publisher_website = url.split('/')[2]       
        publisher = publisher_website.split('.')[-2]  

        # Extract information with default values if not found
        title = response.html.find('h1', first=True).text if response.html.find('h1', first=True) else "No title"
        reporter = response.html.find('.contributor-name', first=True).text if response.html.find('.contributor-name', first=True) else "Unknown"
        
        datetime_element = response.html.find('time', first=True)
        news_datetime = datetime_element.attrs['datetime'] if datetime_element else "Unknown"
        category = response.html.find('.print-entity-section-wrapper', first=True).text if response.html.find('.print-entity-section-wrapper', first=True) else "Uncategorized"

        news_body = '\n'.join([p.text for p in response.html.find('p')]) if response.html.find('p') else "No content"

        img_tags = response.html.find('img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]

        return publisher_website, publisher, title, reporter, news_datetime, category, news_body, images
    except Exception as e:
        print(f"An error occurred while scraping the news article: {e}")
        return None
    finally:
        session.close()

def main():
    conn = create_data_connection()
    if conn is not None:
        try:
            news_urls = [
                "https://www.prothomalo.com/entertainment/drama/vsfm28d2sj",
                "https://www.prothomalo.com/chakri/chakri-suggestion/txzjp2tm2l",
                "https://www.prothomalo.com/lifestyle/health/qlkk7dbt65"
            ]
            
            for url in news_urls:
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
