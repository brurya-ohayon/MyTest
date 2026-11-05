from playwright.sync_api import Page
from pages.login_page import LoginPage


def test_sign_in_page(page: Page):
    sign_in_page = LoginPage(page)
    page.pause()
    sign_in_page.open()


