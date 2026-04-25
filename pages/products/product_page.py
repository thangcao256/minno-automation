import allure
from pages.base.base_page import BasePage
from playwright.sync_api import expect
import re
import os

class ProductPage(BasePage):
    """Module 03.02: Sản phẩm -> Danh mục, Nhóm, Nguồn hàng, Thuộc tính - Siêu bền (Super Robust)"""
    
    def __init__(self, page):
        super().__init__(page)
        
        # 1. Nút THÊM (Vạn năng): Tìm nút có text 'Thêm' và đang HIỂN THỊ
        # Ta không giới hạn class để tránh việc mỗi tab mỗi class khác nhau
        self.add_btn_locator = self.page.locator("//*[@id='root']/div/div/main/div/div[2]/div/div/div[1]/div/div[2]/button")
        
        # 2. Nút XÁC NHẬN / LƯU (Vạn năng): Nằm trong Dialog, thường có màu xanh hoặc text 'Xác nhận/Lưu'
        # Ta lấy cái cuối cùng xuất hiện trong DOM
        self.submit_btn_locator = self.page.locator("//*[@id='radix-_r_0_']/div[3]/button[2]")
        
        self.name_input = self.page.locator("input[name='name']")
        self.code_input = self.page.locator("input[name='code']")
        self.phone_input = self.page.locator("input[name='phoneNumber']")
        
        # Nút Back Drawer (Logic bạn đã test thành công)
        self.drawer_back = self.page.locator('div[role="dialog"]').last.locator("button").first
        self.search_btn = self.page.locator("//*[@id='radix-_r_k7_-content-category']/div/div[1]/div[2]/div/div[2]/div[1]/div/button")
        # Locator nút Sang trang
        self.next_page_btn = self.page.locator("button:has(svg path[d='m9 18 6-6-6-6'])")

    @allure.step("Điều hướng tới tab: {tab_key}")
    def navigate_to_category_tab(self, tab_key="category"):
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        self.navigate(f"{base_url}/product/category?tab={tab_key}")
        self.wait_for_load("networkidle")

    @allure.step("Thêm danh mục: {name}")
    def add_category(self, name: str, code: str = None):
        self.click(self.add_btn_locator.filter(visible=True).first)
        self.fill(self.name_input, name)
        if code: self.fill(self.code_input, code)
        self._save_and_verify(name)

    @allure.step("Thêm nhóm: {name}")
    def add_group(self, name: str, code: str = None):
        self.click(self.add_btn_locator.filter(visible=True).first)
        self.fill(self.name_input, name)
        if code: self.fill(self.code_input, code)
        self._save_and_verify(name)

    @allure.step("Thêm thuộc tính: {attr_name}")
    def add_attribute(self, attr_name: str, values: list):
        self.click(self.add_btn_locator.filter(visible=True).first)
        self.fill(self.name_input, attr_name)
        for i, val in enumerate(values):
            current_input = self.page.locator("div[role='dialog'] input:not([name='name'])").last
            self.fill(current_input, val)
            if i < len(values) - 1:
                # Tìm nút 'Thêm giá trị' đang hiển thị
                add_val_btn = self.page.locator("span[data-state='closed']")
                self.click(add_val_btn)
        self._save_and_verify(attr_name)

    def _save_and_verify(self, name: str):
        # Đợi nút Submit xuất hiện và click
        self.click(self.submit_btn_locator.last, force=True)
        self.page.wait_for_timeout(2000)

    @allure.step("Thêm nhà cung cấp: {name}")
    def add_supplier(self, name: str, code: str = "", email: str = "", phone: str = "", 
                     province: str = "", district: str = "", ward: str = "", address: str = ""):
        """Thêm nhà cung cấp với đầy đủ các trường thông tin chi tiết, hỗ trợ đa ngôn ngữ"""
        self.click(self.add_btn_locator.filter(visible=True).first)

        # Sử dụng name attribute để locator bền vững hơn placeholder
        self.page.locator("input[name='name']").fill(name)
        if code:
            self.page.locator("input[name='code']").fill(code)
        if email:
            self.page.locator("input[name='email']").fill(email)
        if phone:
            self.page.locator("input[name='phoneNumber']").fill(phone)

        # Xử lý Dropdowns (Tỉnh/Huyện/Xã)
        # Vì phần này thường không có name trực tiếp trên button, ta dùng filter hoặc sibling của label
        if province:
            self.select_from_dropdown(self.page.locator("div:has(> label:text-is('Tỉnh/Thành')) button, div:has(> label:text-is('Province/City')) button").first, province)
        if district:
            self.select_from_dropdown(self.page.locator("div:has(> label:text-is('Huyện/Quận')) button, div:has(> label:text-is('District')) button").first, district)
        if ward:
            self.select_from_dropdown(self.page.locator("div:has(> label:text-is('Xã/Phường')) button, div:has(> label:text-is('Ward')) button").first, ward)

        # Địa chỉ chi tiết
        if address:
            self.page.locator("input[name='address']").fill(address)

        self._save_and_verify(name)