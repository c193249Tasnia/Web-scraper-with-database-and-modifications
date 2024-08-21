import requests

def get_example():
    """
    Makes a GET request to a placeholder API and prints the retrieved posts.

    Handles potential request errors including connection issues and timeouts.
    """
    url = 'https://jsonplaceholder.typicode.com/posts'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print("GET request successful!")

        posts = response.json()  # Parse JSON response
        for i, post in enumerate(posts, start=1):
            print(f"Post {i}:")
            print(post)
            print()

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")
    except requests.RequestException as req_err:
        print(f"An error occurred: {req_err}")

def post_example():
    """
    Makes a POST request to a placeholder API with some data and prints the response.

    Handles potential request errors including connection issues and timeouts.
    """
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = {
        'title': 'hello',
        'body': 'this is my post code',
        'userId': 10
    }
    try:
        response = requests.post(url, json=data)
       
