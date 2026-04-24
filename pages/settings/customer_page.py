import allure
from pages.base.base_page import BasePage
import re
import os

class SettingsCustomerPage(BasePage):
    """Module 10.05: Cài đặt -> Khách hàng - Sử dụng 100% BasePage Actions"""
    
    def __init__(self, page):
        super().__init__(page)
        self.add_btn_locator = self.page.get_by_role("button", name=re.compile(r"Thêm|Add", re.I))       
        self.submit_btn = self.page.locator("button[type='submit']")
        self.name_field = self.page.locator("input[name='name'], input:not([type='checkbox'])").first     
        self.drawer_back = self.page.locator('div[role="dialog"]').last.locator("button").first
        self.next_page_btn = self.page.locator("button:has(svg path[d='m9 18 6-6-6-6'])")

    @allure.step("Navigate to Customer Settings tab: {tab_key}")
    def navigate_to_tab(self, tab_key="tag"):
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        self.navigate(f"{base_url}/settings/customer?tab={tab_key}")
        self.wait_for_load("networkidle")

    @allure.step("Create Configuration and Exit: {name}")
    def create_config_and_exit(self, name: str):
        self.click(self.add_btn_locator.filter(visible=True).first)
        self.fill(self.name_field, name)
        self.click(self.submit_btn.first)
        self.page.wait_for_timeout(1000)
        page_num = 1
        while True:
            self.logger.info(f"Searching page {page_num} for '{name}'...")
            item = self.page.get_by_text(name, exact=True).first
            if self.is_visible(item, timeout=2000):
                self.logger.info(f"SUCCESS: Found '{name}' on page {page_num}!")
                break
            
            next_btn = self.next_page_btn.last
            if self.is_visible(next_btn) and next_btn.is_enabled():
                self.click(next_btn, force=True)
                page_num += 1
                self.page.wait_for_timeout(2000)
            else:
                break

        if self.is_visible(self.drawer_back):
            self.click(self.drawer_back, force=True)
            self.logger.info("Closed creation drawer.")
