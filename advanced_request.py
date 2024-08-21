import requests

def get_with_custom_headers():
    """
    Demonstrates a GET request with custom headers and a user agent.
    Fetches data from a public API and prints the JSON response.
    """
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    headers = {
        'User-Agent': 'AdvancedRequestClient/1.0',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("GET request successful!")
        print(response.json())
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def post_with_json_data():
    """
    Demonstrates a POST request that sends JSON data to a public API.
    Prints the response received from the server.
    """
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = {
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    headers = {
        'User-Agent': 'AdvancedRequestClient/1.0',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("POST request successful!")
        print(response.json())
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def main():
    """
    Main function to execute advanced request examples.
    """
    print("Executing GET request with custom headers...")
    get_with_custom_headers()

    print("\nExecuting POST request with JSON data...")
    post_with_json_data()

if __name__ == "__main__":
    main()
