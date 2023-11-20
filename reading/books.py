import os


class Books:
    def __init__(self, provider):
        self.provider = provider

    def get_handler(self):
        try:
            if self.provider == "Google":
                print("Provider Book: Google")
                from .book_google import BookGoogle
                return BookGoogle()

        except BaseException as e:
            raise RuntimeError(e)
