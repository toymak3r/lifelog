# Minimal Book Provider Class

from abc import ABC, abstractmethod


class BookProvider(ABC):

    def __init__(self, provider, params=None):
        self.provider = provider

    @abstractmethod
    def get_book_info_by_isbn(isbn):
        pass

    @abstractmethod
    def get_book_info_by_title(title):
        pass