from playwright.sync_api import Page, expect
import logging
import os
import re
from datetime import datetime

class BasePage:
    """
    LEVEL 5+ SENIOR BASE PAGE
    Encapsulates Smart Actions, Wait Strategies, and a robust Verify Layer.
    """
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def navigate(self, url: str):
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="networkidle")

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False

    def click(self, target, retry: int = 2, force: bool = False, **kwargs):
        self.logger.info(f"Smart Clicking on: {target} (Force={force})")

        for i in range(retry):
            try:
                el = target if hasattr(target, "click") else self.page.locator(target).first

                if not force:
                    el.wait_for(state="visible", timeout=10000)

                el.click(force=force, **kwargs)
                return

            except Exception:
                if i == retry - 1:
                    self.take_screenshot(f"fail_click_{i}")
                    raise
                self.page.wait_for_timeout(500)

    def fill(self, selector: str, value: str, clear: bool = True, **kwargs):
        self.logger.info(f"Filling '{value}' into: {selector}")
        el = self.page.locator(selector).first
        el.wait_for(state="visible", timeout=10000)
        if clear:
            el.fill("")
        el.fill(value, **kwargs)

    def wait_for_load(self, state: str = "networkidle"):
        self.page.wait_for_load_state(state)

    def should_be_visible(self, selector: str, timeout: int = 10000):
        expect(self.page.locator(selector).first).to_be_visible(timeout=timeout)

    def should_have_url(self, expected_url_pattern: str):
        expect(self.page).to_have_url(expected_url_pattern)

    def take_screenshot(self, name: str = "screenshot"):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"
        self.page.screenshot(path=path)
