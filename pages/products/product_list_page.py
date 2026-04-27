import allure
from pages.base.base_page import BasePage
from playwright.sync_api import expect
import re

class ProductListPage(BasePage):
    """
    Module 03.01: Sản phẩm -> Danh sách sản phẩm
    Xử lý tìm kiếm tự động và xác nhận thông tin sản phẩm.
    """

    def __init__(self, page):
        super().__init__(page)
        
        # --- Locators ---
        # Nút Search: Nhắm vào button chứa icon SVG 'bi-search'
        self.search_btn = self.page.locator("button:has(svg.bi-search), button:has(svg path[d*='M11.742'])")
        # Ô nhập Search (Dựa trên placeholder)
        self.search_input = self.page.get_by_placeholder(re.compile(r"Search|Tìm kiếm", re.I))
        
        self.table_rows = self.page.locator("table tbody tr")
        
        # Các cột trong bảng (dựa trên cấu hình mặc định)
        self.col_name = 2  # Cột 3 (0-indexed: 2)
        self.col_status = 3
        self.col_stock = 4
        self.col_cost = 5
        self.col_price = 6

    @allure.step("Tìm kiếm sản phẩm: {keyword}")
    def search(self, keyword: str):
        self._log(f"Searching for product: {keyword}")
        
        # 1. Click vào icon Tìm kiếm nếu ô nhập chưa hiện
        if not self.search_input.is_visible():
            if self.is_visible(self.search_btn):
                self.click(self.search_btn)
                self.wait(0.5)

        # 2. Nhập từ khóa
        target_input = self.search_input.filter(visible=True).first
        self.fill_smart(target_input, keyword)
        
        # 3. Đợi Spinner biến mất (nếu có)
        self.wait_for_spinner()
        # Quan trọng: Đợi một chút để React debounce search
        self.wait(2.0) 

    @allure.step("Xác nhận sản phẩm hiển thị trong danh sách")
    def verify_product_in_list(self, name: str, sku: str = None, price: str = None, stock: str = None):
        """Kiểm tra dòng đầu tiên của kết quả tìm kiếm với cơ chế tự động đợi"""
        self._log(f"Verifying product '{name}' in the first row.")
        
        # Nhắm vào cell tên của dòng đầu tiên
        name_cell = self.table_rows.first.locator("td").nth(self.col_name)
        
        # Sử dụng expect với timeout lớn để Playwright tự động retry cho đến khi Search xong
        # Điều này giúp tránh việc lấy nhầm dữ liệu cũ chưa kịp biến mất
        expect(name_cell).to_contain_text(name, timeout=15000)
        self._log("Product verification successful.")

    @allure.step("Mở chi tiết sản phẩm đầu tiên")
    def open_first_product(self):
        self.table_rows.first.click()
        self.wait_for_load()
