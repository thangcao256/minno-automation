import allure
from pages.base.base_page import BasePage
import os

class SettingsRankPage(BasePage):
    """Module 10.06: Cài đặt -> Hạng khách hàng (Loyalty Ranks)"""
    
    def __init__(self, page):
        super().__init__(page)
        self.add_button = "button:has-text('Thêm'), button:has-text('Thêm mới')"
        self.name_input = "input[name='name']"
        self.min_spend_input = "input[name='minSpend']"
        self.discount_input = "input[name='discount']"
        self.submit_button = "button[type='submit']"

    @allure.step("Navigate to Customer Ranks page")
    def navigate_to_ranks(self):
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        # URL cho trang Hạng khách hàng riêng biệt
        self.navigate(f"{base_url}/settings/customer-ranks")

    @allure.step("Create a new Customer Rank: {1}")
    def create_rank(self, name: str, min_spend: str, discount: str):
        self.click(self.add_button)
        self.fill(self.name_input, name)
        self.fill(self.min_spend_input, min_spend)
        self.fill(self.discount_input, discount)
        self.click(self.submit_button)
        self.should_be_visible(f"text='{name}'")
