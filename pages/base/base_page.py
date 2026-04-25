from playwright.sync_api import Page, Locator, expect
import logging
import os
from datetime import datetime
from typing import Union


Target = Union[str, Locator]


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    # =========================
    # 🔹 CORE UTILS
    # =========================
    def _get_locator(self, target: Target) -> Locator:
        if isinstance(target, Locator):
            return target
        return self.page.locator(target).first

    def _log(self, message: str):
        self.logger.info(message)

    # =========================
    # 🔹 NAVIGATION
    # =========================
    def navigate(self, url: str):
        self._log(f"Navigate to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def wait_for_load(self, state: str = "networkidle"):
        self.page.wait_for_load_state(state)

    # =========================
    # 🔹 SMART ACTIONS
    # =========================
    def click(self, target: Target, retry: int = 2, force: bool = False):
        el = self._get_locator(target)

        for i in range(retry):
            try:
                self._log(f"Click: {target} (attempt {i+1})")

                el.wait_for(state="visible", timeout=10000)
                el.scroll_into_view_if_needed()
                expect(el).to_be_enabled()

                el.click(force=force)
                return

            except Exception as e:
                self._log(f"Click failed: {e}")

                if i == retry - 1:
                    self.take_screenshot("fail_click")
                    raise

                self.wait_for_load()

    def fill(self, target: Target, value: str):
        el = self._get_locator(target)

        self._log(f"Fill '{value}' into: {target}")

        el.wait_for(state="visible", timeout=10000)
        el.scroll_into_view_if_needed()

        el.clear()
        el.fill(value)

    def hover(self, target: Target):
        el = self._get_locator(target)
        el.wait_for(state="visible")
        el.hover()

    def press(self, target: Target, key: str):
        el = self._get_locator(target)
        el.press(key)

    def select_option(self, target: Target, value: str):
        el = self._get_locator(target)
        el.select_option(value)

    def upload_file(self, target: Target, file_path: str):
        el = self._get_locator(target)
        el.set_input_files(file_path)

    # =========================
    # 🔹 GETTERS
    # =========================
    def get_text(self, target: Target) -> str:
        el = self._get_locator(target)
        el.wait_for(state="visible")
        return el.inner_text()

    def is_visible(self, target: Target, timeout: int = 5000) -> bool:
        try:
            el = self._get_locator(target)
            el.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    # =========================
    # 🔹 WAIT HELPERS
    # =========================
    def wait_for_element(self, target: Target, timeout: int = 10000):
        el = self._get_locator(target)
        el.wait_for(state="visible", timeout=timeout)

    def wait_for_text(self, target: Target, text: str):
        el = self._get_locator(target)
        expect(el).to_contain_text(text)

    def wait_for_url(self, url_pattern: str):
        self.page.wait_for_url(url_pattern)

    def wait(self, seconds: float):
        self.page.wait_for_timeout(int(seconds * 1000))

    # =========================
    # 🔹 ASSERT / VERIFY LAYER
    # =========================
    def should_be_visible(self, target: Target, timeout: int = 10000):
        el = self._get_locator(target)
        expect(el).to_be_visible(timeout=timeout)

    def should_have_text(self, target: Target, expected: str):
        el = self._get_locator(target)
        expect(el).to_have_text(expected)

    def should_contain_text(self, target: Target, expected: str):
        el = self._get_locator(target)
        expect(el).to_contain_text(expected)

    def should_have_url(self, expected_url_pattern: str):
        expect(self.page).to_have_url(expected_url_pattern)

    # =========================
    # 🔹 DEBUG & UTILITIES
    # =========================
    def highlight(self, target: Target):
        el = self._get_locator(target)
        el.highlight()

    def count(self, target: Target) -> int:
        return self.page.locator(target).count() if isinstance(target, str) else target.count()

    def take_screenshot(self, name: str = "screenshot"):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"
        self.page.screenshot(path=path)
        self._log(f"Screenshot saved: {path}")

    def select_from_dropdown(self, trigger_target: Target, option_name: str):
        """Hỗ trợ chọn option từ custom dropdown (Radix/Shadcn) có hỗ trợ cuộn"""
        self._log(f"Selecting option '{option_name}' from dropdown: {trigger_target}")
        
        # 1. Click mở dropdown
        self.click(trigger_target)
        
        # 2. Tìm option. Radix thường render list trong Portal (cuối body)
        # Ta dùng locator tìm theo role option hoặc text
        option_locator = self.page.get_by_role("option", name=re.compile(f".*{option_name}.*", re.I)).first
        
        # Nếu không tìm thấy theo role, thử tìm theo text đơn thuần trong các popup/viewport
        if not self.is_visible(option_locator, timeout=2000):
            option_locator = self.page.locator("[role='listbox'], .radix-select-content").get_by_text(option_name, exact=False).first

        # 3. Cuộn và Click
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.wait_for_load("domcontentloaded")

    def try_click(self, target: Target, timeout: int = 3000) -> bool:
        try:
            el = self._get_locator(target)
            el.wait_for(state="visible", timeout=timeout)
            el.click()
            return True
        except:
            return False