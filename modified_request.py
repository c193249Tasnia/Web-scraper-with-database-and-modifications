import requests

def get_example():
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        print("GET request successful!")

        # Extracting JSON data
        posts = response.json()
        
        # Print titles of all posts
        print("Titles of all posts:")
        for i, post in enumerate(posts, start=1):
            print(f"Post {i} title: {post['title']}")
    else:
        print("Failed to retrieve data")

def main():
    print("Executing GET example...")
    get_example()

if __name__ == "__main__":
    main()
