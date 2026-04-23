import allure
from pages.base.base_page import BasePage
import os

class MarketingPage(BasePage):
    """Handles Promotions and Vouchers in Module 07: Marketing"""
    
    def __init__(self, page):
        super().__init__(page)
        self.promotion_name_input = "input[placeholder='Tên chương trình']"
        self.voucher_code_input = "input[placeholder='Mã voucher']"
        self.discount_value_input = "input[name='discountValue']"
        self.save_button = "button:has-text('Lưu'), button:has-text('Xác nhận')"

    @allure.step("Navigate to New Promotion page")
    def navigate_to_new_promotion(self):
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        self.navigate(f"{base_url}/dashboard/promotions/new")

    @allure.step("Create a new promotion: {1}")
    def create_promotion(self, name: str):
        self.fill(self.promotion_name_input, name)
        self.click(self.save_button)
        self.should_contain_text("body", "thành công") # Generic success verification

    @allure.step("Navigate to New Voucher page")
    def navigate_to_new_voucher(self):
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        self.navigate(f"{base_url}/dashboard/promotions/vouchers/new")

    @allure.step("Create a new voucher: {1} with {2}% discount")
    def create_voucher(self, code: str, discount: str):
        self.fill(self.voucher_code_input, code)
        self.fill(self.discount_value_input, discount)
        self.click(self.save_button)
        self.should_contain_text("body", "thành công")
