import allure
from pages.base.base_page import BasePage
import re

class ProductCreatePage(BasePage):
    """
    Module 03.01: Sản phẩm -> Thêm mới sản phẩm
    Sử dụng các phương thức nâng cấp từ BasePage để xử lý React UI.
    """
    
    def __init__(self, page):
        super().__init__(page)
        
        # --- Locators: Text Fields ---
        self.name_input = "input[name='name']"
        self.sku_input = "input[name='SKU_code']"
        self.bar_code_input = "input[name='bar_code']"
        self.note_textarea = "textarea[name='note']"

        # --- Locators: Radio / Switches ---
        self.radio_is_saleable_yes = self.page.locator("div").filter(has_text=re.compile(r"Dùng để bán|For sale", re.I)).locator("button[role='radio']").first
        
        self.radio_stock_yes = self.page.locator("div").filter(has_text=re.compile(r"^Có$|^Yes$", re.I)).locator("button[role='radio']")
        self.radio_negative_stock_yes = self.page.locator("div").filter(has_text=re.compile(r"Cho phép bán âm|Allow negative stock", re.I)).locator("button[role='radio']")

        # --- Locators: Dropdowns (Mapped by reverse order) ---
        self.all_comboboxes = self.page.get_by_role("combobox")
        self.status_dropdown = self.all_comboboxes.nth(-4)   # is_active
        self.group_dropdown = self.all_comboboxes.nth(-3)    # group_id
        self.category_dropdown = self.all_comboboxes.nth(-2) # category_id
        self.supplier_dropdown = self.all_comboboxes.nth(-1) # supplier_id

        # --- Locators: Buttons ---
        self.save_btn = self.page.get_by_role("button", name=re.compile(r"^Lưu$|^Save$", re.I))

    @allure.step("Nhập thông tin sản phẩm theo Schema API")
    def fill_product_data(self, product_data: dict):
        # 1. Thông tin văn bản cơ bản
        self.fill(self.name_input, product_data.get('name', ''))
        if 'SKU_code' in product_data: self.fill(self.sku_input, product_data['SKU_code'])
        if 'bar_code' in product_data: self.fill(self.bar_code_input, product_data['bar_code'])
        if 'note' in product_data: self.fill(self.note_textarea, product_data['note'])

        # 2. Giá cả & Số lượng (Sử dụng fill_by_label siêu ổn định)
        if 'purchase_price' in product_data:
            self.fill_by_label("Wholesale price", str(product_data['purchase_price']))
        
        if 'sale_price' in product_data:
            self.fill_by_label("Sale price", str(product_data['sale_price']))

        self.wait_for_spinner()

        self.wait(6000)
        # 3. Trạng thái kinh doanh & Kho
        # Is the product for sale?
        if product_data.get('is_saleable') is False:
            self.click(self.radio_is_saleable_yes)
        
        if product_data.get('is_required_inventory') is True:
            self.click(self.radio_stock_yes)
            if 'inventory_quantity' in product_data:
                self.fill_by_label("Số lượng", str(product_data['inventory_quantity']))
            
            if product_data.get('allow_negative_stock') is True:
                self.click(self.radio_negative_stock_yes)

        # 4. Phân loại (Dropdowns)
        if 'group' in product_data: self.select_from_dropdown(self.group_dropdown, product_data['group'])
        if 'category' in product_data: self.select_from_dropdown(self.category_dropdown, product_data['category'])
        if 'supplier' in product_data: self.select_from_dropdown(self.supplier_dropdown, product_data['supplier'])
        if 'status' in product_data: self.select_from_dropdown(self.status_dropdown, product_data['status'])

    @allure.step("Nhấn Lưu sản phẩm")
    def save(self):
        self.click(self.save_btn.filter(visible=True).first)
        self.page.wait_for_url(re.compile(r".*/products$|.*/products/.*"), timeout=15000)
