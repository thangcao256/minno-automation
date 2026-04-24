import allure
from pages.base.base_page import BasePage
from playwright.sync_api import expect
import re

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # --- Locators ---
        self.logo = "img[alt='Logo']"
        self.search_button = "button:has-text('⌘K')"
        self.user_menu_avatar = "button[aria-haspopup='menu']"
        self.logout_item = self.page.get_by_role("menuitem", name=re.compile(r"Logout|Đăng xuất", re.I))

    @allure.step("Verify Dashboard is ready")
    def verify_dashboard_ready(self):
        self.should_be_visible(self.logo)
        self.should_be_visible(self.search_button)

    @allure.step("Perform Logout from User Menu")
    def logout(self):
        """
        Scenario: Click Avatar -> Click Logout (via stored locator) -> Verify redirection
        """
        # 1. Open User Menu
        self.click(self.user_menu_avatar)
        
        # 2. Click Logout button (đã được khai báo ở trên)
        self.logger.info("Clicking on Logout menu item")
        self.logout_item.click()
        
        # 3. Verify redirection
        self.page.wait_for_url(re.compile(r".*/auth/.*"))
        self.logger.info("Logout successful.")
