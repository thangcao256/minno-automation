import allure
from pages.base.base_page import BasePage
import re

class ProductCreatePage(BasePage):
    """
    Module 03.01: Sản phẩm -> Thêm mới sản phẩm
    Hoàn thiện dựa trên phân tích UI và Schema API POST /products/
    """
    
    def __init__(self, page):
        super().__init__(page)
        
        # --- Locators: Text Fields (Mapped to API Schema) ---
        self.name_input = "input[name='name']"             # API: name
        self.sku_input = "input[name='SKU_code']"         # API: SKU_code
        self.bar_code_input = "input[name='bar_code']"     # API: bar_code
        self.note_textarea = "textarea[name='note']"       # API: note
        
        # --- Locators: Prices (API: purchase_price & sale_price) ---
        # Bắt theo container chứa ký hiệu tiền tệ 'đ'
        self.price_inputs = self.page.locator("div").filter(has=self.page.get_by_text("đ", exact=True)).locator("input")
        self.purchase_price_input = self.price_inputs.first  # API: purchase_price (Giá vốn)
        self.sale_price_input = self.price_inputs.nth(1)    # API: sale_price (Giá bán)
        
        # --- Locators: Radio / Switches (API booleans) ---
        # is_saleable: Dùng để bán
        self.radio_is_saleable_yes = self.page.locator("div").filter(has_text=re.compile(r"Dùng để bán|For sale", re.I)).locator("button[role='radio']").first
        
        # is_required_inventory: Quản lý tồn kho
        self.stock_section = self.page.locator("div").filter(has_text=re.compile(r"Quản lý tồn kho|Stock management", re.I))
        self.radio_stock_yes = self.page.locator("div").filter(has_text=re.compile(r"^Có$|^Yes$", re.I)).locator("button[role='radio']")
        self.radio_stock_no = self.page.locator("div").filter(has_text=re.compile(r"^Không$|^No$", re.I)).locator("button[role='radio']")

        # allow_negative_stock: Cho phép bán âm (Thường ẩn/hiện tùy option kho)
        self.radio_negative_stock_yes = self.page.locator("div").filter(has_text=re.compile(r"Cho phép bán âm|Allow negative stock", re.I)).locator("button[role='radio']")

        # --- Locators: Dropdowns (UUID relations) ---
        self.all_comboboxes = self.page.get_by_role("combobox")
        self.status_dropdown = self.all_comboboxes.nth(-4)   # is_active
        self.group_dropdown = self.all_comboboxes.nth(-3)    # group_id
        self.category_dropdown = self.all_comboboxes.nth(-2) # category_id
        self.supplier_dropdown = self.all_comboboxes.nth(-1) # supplier_id

        # --- Locators: Buttons ---
        self.save_btn = self.page.get_by_role("button", name=re.compile(r"^Lưu$|^Save$", re.I))
        self.add_variant_btn = self.page.get_by_role("button", name=re.compile(r"Thêm thuộc tính khác|Add another attribute", re.I))

    @allure.step("Nhập thông tin sản phẩm theo Schema API")
    def fill_product_data(self, product_data: dict):
        """
        Điền form dựa trên cấu trúc API:
        {
            'name': str, 'SKU_code': str, 'bar_code': str,
            'purchase_price': float, 'sale_price': float,
            'is_saleable': bool, 'is_required_inventory': bool,
            'allow_negative_stock': bool, 'inventory_quantity': int,
            'category': str, 'supplier': str, 'group': str, 'status': str
        }
        """
        # 1. Thông tin văn bản chính
        self.fill(self.name_input, product_data.get('name', ''))
        if 'SKU_code' in product_data: self.fill(self.sku_input, product_data['SKU_code'])
        if 'bar_code' in product_data: self.fill(self.bar_code_input, product_data['bar_code'])
        if 'note' in product_data: self.fill(self.note_textarea, product_data['note'])
            
        # 2. Tài chính
        if 'sale_price' in product_data: self.fill(self.sale_price_input, str(product_data['sale_price']))
        if 'purchase_price' in product_data: self.fill(self.purchase_price_input, str(product_data['purchase_price']))
            
        # 3. Trạng thái kinh doanh & Kho
        if product_data.get('is_saleable') is False:
            self.click(self.radio_is_saleable_yes) # Toggle off
        
        if product_data.get('is_required_inventory') is True:
            self.click(self.radio_stock_yes)
            # Điền số lượng ban đầu (inventory_quantity)
            if 'inventory_quantity' in product_data:
                qty_input = self.page.locator("div:has(> label:text-is('Số lượng')) input, div:has(> label:text-is('Quantity')) input").first
                self.fill(qty_input, str(product_data['inventory_quantity']))
            
            # Cho phép bán âm
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
        # Chờ điều hướng để xác nhận hoàn tất
        self.page.wait_for_url(re.compile(r".*/products$|.*/products/.*"), timeout=15000)
