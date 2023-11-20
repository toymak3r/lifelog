"""
This code snippet initializes the `actual_date` variable with the current date and creates an instance of the `Config` class called `configuration`.

Example Usage:

    actual_date = date.today()
    configuration = Config()

Inputs:
    None

Outputs:
    None
"""

from datetime import date
from config import Config
from reading.books import Books

actual_date = date.today()
configuration = Config()
books = Books('Google').get_handler()
books.get_book_info_by_isbn('1506724884')
books.get_book_info_by_title('Creeping')