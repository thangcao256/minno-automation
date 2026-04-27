import re
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

    def wait_for_spinner(self, timeout: int = 15000):
        """Đợi cho các spinner/loading biến mất"""
        try:
            spinner = self.page.locator(".animate-spin, .loading-spinner, [role='status']").first
            if spinner.is_visible():
                spinner.wait_for(state="hidden", timeout=timeout)
        except:
            pass

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
        """Basic fill with auto-clear"""
        el = self._get_locator(target)
        self._log(f"Fill '{value}' into: {target}")
        el.wait_for(state="visible", timeout=10000)
        el.scroll_into_view_if_needed()
        el.fill(value)

    def fill_smart(self, target: Target, value: str):
        """Nâng cao: Xóa bằng phím tắt để kích hoạt React state change"""
        el = self._get_locator(target)
        self._log(f"Smart Fill '{value}' into: {target}")
        el.wait_for(state="visible", timeout=10000)
        el.click()
        # Ctrl+A -> Backspace
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        el.type(value, delay=50) # Type chậm hơn một chút để React kịp bắt event

    def fill_by_label(self, label_text: str, value: str, is_exact: bool = False):
        """Điền input dựa trên Label - Cực kỳ ổn định cho React"""
        self._log(f"Fill by label '{label_text}': {value}")
        
        # Tạo các mẫu tìm kiếm: Tuyệt đối trước, Gần đúng sau
        patterns = [
            re.compile(f"^{label_text}$", re.I),
            re.compile(f".*{label_text}.*", re.I)
        ]
        
        target_el = None
        for pattern in patterns:
            # Các chiến thuật từ chính xác đến linh hoạt
            strategies = [
                lambda p=pattern: self.page.get_by_label(p, exact=True),
                lambda p=pattern: self.page.get_by_role("textbox", name=p),
                lambda p=pattern: self.page.get_by_role("spinbutton", name=p),
                # Chiến thuật vùng chứa hẹp: tìm div nhỏ nhất chứa label và có input
                lambda p=pattern: self.page.locator("div.space-y-1, .flex, .grid, fieldset").filter(has=self.page.get_by_text(p, exact=True)).locator("input, textarea, [role='textbox'], [role='spinbutton']").first
            ]

            for i, strategy in enumerate(strategies):
                try:
                    locator = strategy()
                    # Kiểm tra thực sự có element và nó đang hiển thị
                    if locator.count() > 0:
                        locator.wait_for(state="visible", timeout=2000)
                        target_el = locator
                        self._log(f"Strategy {i+1} succeeded for label '{label_text}' with pattern '{pattern.pattern}'")
                        break
                except:
                    continue
            
            if target_el:
                break

        if target_el:
            self.fill_smart(target_el, value)
        else:
            # Dự phòng cuối cùng: dùng get_by_label mặc định để lấy log lỗi chuẩn
            self._log(f"All strategies failed for '{label_text}', trying final fallback...")
            self.fill_smart(self.page.get_by_label(label_text), value)

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

    def select_from_dropdown(self, trigger_target: Target, option_name: str = ""):
        """
        Hỗ trợ chọn option từ custom dropdown:
        - Ưu tiên tìm khớp gần đúng theo option_name.
        - Nếu không thấy hoặc option_name trống, chọn cái đầu tiên.
        """
        self._log(f"Selecting option '{option_name}' from dropdown: {trigger_target}")
        
        # 1. Click mở dropdown
        self.click(trigger_target)
        self.page.wait_for_timeout(500) # Đợi animation mở popup

        # 2. Xử lý tìm kiếm và chọn
        found = False
        if option_name:
            # Thử tìm theo role='option' có chứa text (không phân biệt hoa thường)
            # Dùng regex để khớp gần đúng
            option_locator = self.page.get_by_role("option").filter(has_text=re.compile(f".*{option_name}.*", re.I)).first
            
            if self.is_visible(option_locator, timeout=2000):
                option_locator.scroll_into_view_if_needed()
                option_locator.click()
                found = True
        
        if not found:
            self._log("Option not found or not provided, selecting the first available option.")
            # Chọn cái đầu tiên trong listbox
            first_option = self.page.get_by_role("option").first
            if self.is_visible(first_option, timeout=2000):
                first_option.scroll_into_view_if_needed()
                first_option.click()
            else:
                # Dự phòng nếu không dùng role option (ví dụ custom div)
                fallback_first = self.page.locator("[role='listbox'] div, .radix-select-content div").first
                fallback_first.click()

        self.wait_for_load("domcontentloaded")

    def try_click(self, target: Target, timeout: int = 3000) -> bool:
        try:
            el = self._get_locator(target)
            el.wait_for(state="visible", timeout=timeout)
            el.click()
            return True
        except:
            return False