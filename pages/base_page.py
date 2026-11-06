from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = f"{base_url}/"

    def go(self, path: str = ""):
        self.page.goto(f"{self.base_url}{path}")
