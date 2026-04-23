import allure
from pages.base.base_page import BasePage
import re
import os

class SettingsCustomerPage(BasePage):
    """Module 10.05: Cài đặt -> Khách hàng (Bản khôi phục trạng thái PASSED)"""
    
    def __init__(self, page):
        super().__init__(page)
        # Đây là bộ chọn đã giúp bạn PASS 2 test case trước đó
        self.add_btn = self.page.locator("button").filter(has_text=re.compile(r"Add|Thêm", re.I))
        self.submit_btn = self.page.locator("button[type='submit']")
        self.name_field = self.page.locator("input[name='name'], input:not([type='checkbox'])").first
        
        # Thêm nút thoát bền vững (Nút X ở góc Drawer)
        self.exit_btn = self.page.locator("button").filter(has=self.page.locator("[data-lucide='x']")).first

    @allure.step("Navigate to Customer Settings tab: {1}")
    def navigate_to_tab(self, tab_key="tag"):
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        self.navigate(f"{base_url}/settings/customer?tab={tab_key}")
        self.wait_for_load("networkidle")

    @allure.step("Create Configuration and Exit: {1}")
    def create_config_and_exit(self, name: str):
        """Sử dụng đúng logic đã PASS và thêm bước Thoát nhẹ nhàng"""
        # 1. Click Thêm (Dùng .first để tránh lỗi đa phần tử)
        self.add_btn.first.click()
        
        # 2. Điền tên
        self.name_field.fill(name)
        
        # 3. Lưu
        self.submit_btn.first.click()
        
        # 4. Xác nhận thành công
        self.should_be_visible(f"text='{name}'")
        
        # 5. Thoát Drawer (Nếu có nút X thì bấm, không thì thôi để không gây lỗi test)
        try:
            if self.exit_btn.is_visible(timeout=2000):
                self.exit_btn.click()
        except:
            self.page.keyboard.press("Escape")
            self.logger.info("Closed drawer using Escape key.")
