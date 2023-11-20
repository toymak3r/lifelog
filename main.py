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
from jinja2 import Environment, PackageLoader, select_autoescape
from config import Config
from reading.books import Books
from daylog.daylog import Daylog

env = Environment(
    loader=PackageLoader("daylog"),
    autoescape=select_autoescape()
)

configuration = Config()
config = configuration.config
print(config)
daylog = Daylog(config=config, env=env, template='daily_notes.md')
daylog.load()
daylog.save()
#books = Books('Google').get_handler()
#books.get_book_info_by_isbn('1506724884')
#books.get_book_info_by_title('Creeping')
