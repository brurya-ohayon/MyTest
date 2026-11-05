from playwright.sync_api import Page


class BasePage:
    URL = None


    def __init__(self, page: Page):
        self.page = page


    def open(self):
        if self.URL is None:
            raise NotImplementedError(f"{type(self).__name__} must define URL")
        self.page.goto(self.URL)