import os
from requests_html import HTMLSession

# Set the Chromium revision environment variable for Pyppeteer
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

def render_javascript(url):
    """
    Renders JavaScript on a web page and prints the rendered HTML.

    Parameters
    ----------
    url : str
        The URL of the web page to be rendered.

    Raises
    ------
    Exception
        If an error occurs during the request or rendering.
    """
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render(retries=3, sleep=5, wait=10)  # Render JavaScript content
        print("Rendered web page:")
        print(response.html.html)  # Print the rendered HTML
    except Exception as e:
        print(f"An error occurred while rendering JavaScript: {e}")
    finally:
        session.close()

def extract_information(url):
    """
    Extracts information from a web page including title and all links.

    Parameters
    ----------
    url : str
        The URL of the web page to extract information from.

    Raises
    ------
    Exception
        If an error occurs during the request or 
