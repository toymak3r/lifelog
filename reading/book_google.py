
# Using Google Books
import requests
import pprint
from reading.book_provider import BookProvider

pp = pprint.PrettyPrinter(indent=4)

class BookGoogle(BookProvider):
    def __init__(self):
        super().__init__('BookGoogle')

    # Retrieve infos by ISBN
    def get_book_info_by_isbn(self, isbn):
        base_url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": f"isbn:{isbn}"}

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if "items" in data:
                #pp.pprint(data)
                book_info = data["items"][0]["volumeInfo"]
                title = book_info.get("title", "Title not available")
                authors = book_info.get("authors", ["Author not available"])
                publisher = book_info.get(
                    "publisher", "Publisher not available")
                published_date = book_info.get(
                    "publishedDate", "Publication date not available")
                description = book_info.get("description", "Description not available")
                print(f"Title: {title}")
                print(f"Authors: {', '.join(authors)}")
                print(f"Publisher: {publisher}")
                print(f"Published Date: {published_date}")
                print(f"Description: {description}")

            else:
                print("Book not found.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching book information: {e}")

    def get_book_info_by_title(self, title):
        base_url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": f"title:{title}"}

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if "items" in data:
                #pp.pprint(data)
                book_info = data["items"][0]["volumeInfo"]
                title = book_info.get("title", "Title not available")
                authors = book_info.get("authors", ["Author not available"])
                publisher = book_info.get(
                    "publisher", "Publisher not available")
                published_date = book_info.get(
                    "publishedDate", "Publication date not available")
                description = book_info.get("description", "Description not available")
                print(f"Title: {title}")
                print(f"Authors: {', '.join(authors)}")
                print(f"Publisher: {publisher}")
                print(f"Published Date: {published_date}")
                print(f"Description: {description}")

            else:
                print("Book not found.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching book information: {e}")