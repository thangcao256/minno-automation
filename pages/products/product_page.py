from pages.base.base_page import BasePage
from playwright.sync_api import expect
import re

class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_button = "button:has-text('Thêm')"
        self.save_button = "button:has-text('Lưu'), button:has-text('Xác nhận')"
        self.name_input = "input[name='name']"
        self.code_input = "input[name='code']"

    def add_category(self, name, code=None):
        self.click(self.add_button)
        self.fill(self.name_input, name)
        if code:
            self.fill(self.code_input, code)
        self.click(self.save_button)
        # Chờ item mới xuất hiện trong list
        expect(self.page.get_by_text(name).first).to_be_visible()

    def add_attribute(self, attr_name, values: list):
        self.click(self.add_button)
        self.fill(self.name_input, attr_name)
        
        for i, val in enumerate(values):
            # Điền vào ô input cuối cùng
            current_input = self.page.locator("div[role='dialog'] input:not([name='name'])").last
            current_input.fill(val)
            if i < len(values) - 1:
                # Bấm "Thêm giá trị" - Thường là một span hoặc button có text Thêm
                self.page.get_by_text("Thêm giá trị").click()
        
        self.click(self.save_button)
        expect(self.page.get_by_text(attr_name).first).to_be_visible()
