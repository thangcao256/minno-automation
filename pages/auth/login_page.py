from pages.base.base_page import BasePage
from playwright.sync_api import Page, expect
import re

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators (Bền vững)
        self.username_input = "input:not([type='password'])"
        self.password_input = "input[type='password']"
        self.submit_button = "button[type='submit']"
        self.logo = "img[alt='Logo']"
        self.select_store_pattern = re.compile(r".*/auth/select-stores.*")

    def login(self, username, password):
        """Thực hiện luồng đăng nhập 2 bước của MinnoSoft"""
        # Bước 1: Username
        self.fill(self.username_input, username)
        self.page.keyboard.press("Enter")
        
        # Bước 2: Password
        self.fill(self.password_input, password)
        self.click(self.submit_button)

    def select_store(self, store_name: str):
        """Chọn chi nhánh"""
        self.page.wait_for_url(self.select_store_pattern, timeout=15000)
        # Tìm button có chứa text chi nhánh
        store_btn = self.page.locator("button").filter(has_text=store_name).first
        if store_btn.is_visible():
            store_btn.click()
        else:
            # Dự phòng chọn chi nhánh đầu tiên
            self.click("button.flex.items-center.w-full")

    def verify_login_success(self):
        """Kiểm tra login thành công bằng cách đợi Logo hiện lên"""
        expect(self.page.locator(self.logo).first).to_be_visible(timeout=30000)
        expect(self.page).to_have_url(re.compile(r".*dashboard.*"))
