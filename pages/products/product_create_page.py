import allure
from pages.base.base_page import BasePage
import re

class ProductCreatePage(BasePage):
    """
    Module 03.01: Sản phẩm -> Thêm mới sản phẩm
    Hỗ trợ: Biến thể (Variants), Quản lý kho (Inventory), Lô/Hạn dùng (Batch/Expiry), Upload Ảnh
    """

    def __init__(self, page):
        super().__init__(page)

        # --- Locators: Basic Info ---
        self.name_input = "input[name='name']"
        self.sku_input = "input[name='SKU_code']"
        self.bar_code_input = "input[name='bar_code']"
        self.note_textarea = "textarea[name='note']"
        self.file_input = "input[type='file']"

        # --- Locators: Radio Options (Dynamic by text) ---
        def get_radio(text):
            return self.page.locator("div").filter(has_text=re.compile(f"^{text}$", re.I)).locator("button[role='radio']").first

        # Is the product for sale?
        self.radio_for_sale = get_radio("For sale")
        self.radio_internal_use = get_radio("For internal use")

        # Does the product have multiple variants?
        self.radio_variant_no = get_radio("No")
        self.radio_variant_yes = get_radio("Yes")

        # Does the product manage inventory?
        self.radio_inv_no = get_radio("No tracking")
        self.radio_inv_tracking = get_radio("Tracking")

        # Allow negative inventory?
        self.radio_negative_no = get_radio("Not allowed")
        self.radio_negative_allow = get_radio("Allow")

        # --- Locators: Buttons ---
        self.save_btn = self.page.get_by_role("button", name=re.compile(r"^Save$|^Lưu$", re.I))
        self.enter_quantity_btn = self.page.get_by_role("button", name=re.compile(r"Enter quantity", re.I))

        # --- Locators: Dropdowns ---
        self.all_comboboxes = self.page.get_by_role("combobox")
        self.status_dropdown = self.all_comboboxes.nth(-4)
        self.group_dropdown = self.all_comboboxes.nth(-3)
        self.category_dropdown = self.all_comboboxes.nth(-2)
        self.supplier_dropdown = self.all_comboboxes.nth(-1)

    @allure.step("Tải ảnh sản phẩm lên")
    def upload_images(self, file_paths: list):
        if not file_paths:
            return
        self.page.set_input_files(self.file_input, file_paths)
        self.wait(1)

    @allure.step("Nhập thông tin sản phẩm đầy đủ")
    def fill_product_data(self, data: dict):
        # 1. Thông tin cơ bản & Ảnh
        self.fill(self.name_input, data.get('name', ''))
        if 'SKU' in data: self.fill(self.sku_input, data['SKU'])
        if 'barcode' in data: self.fill(self.bar_code_input, data['barcode'])
        if 'note' in data: self.fill(self.note_textarea, data['note'])
        if 'images' in data: self.upload_images(data['images'])

        # 2. Phân loại
        if 'group' in data: self.select_from_dropdown(self.group_dropdown, data['group'])
        if 'category' in data: self.select_from_dropdown(self.category_dropdown, data['category'])
        if 'supplier' in data: self.select_from_dropdown(self.supplier_dropdown, data['supplier'])
        if 'status' in data: self.select_from_dropdown(self.status_dropdown, data['status'])

        # 3. Trạng thái kinh doanh
        if data.get('for_sale') is False:
            self.click(self.radio_internal_use)
        else:
            self.click(self.radio_for_sale)

        # 4. Biến thể
        has_variants = data.get('has_variants', False)
        if has_variants:
            self.click(self.radio_variant_yes)
            self._setup_variants(data.get('variants_config', []))
        else:
            self.click(self.radio_variant_no)
            if 'wholesale_price' in data: self.fill_by_label("Wholesale price", str(data['wholesale_price']))
            if 'sale_price' in data: self.fill_by_label("Sale price", str(data['sale_price']))

        # 5. Quản lý kho
        if data.get('manage_inventory'):
            self.click(self.radio_inv_tracking)
            
            # Luôn kiểm tra nút Enter quantity dù có biến thể hay không
            if self.is_visible(self.enter_quantity_btn):
                self.click(self.enter_quantity_btn)
                self._fill_inventory_setup_dialog(data)
            
            # Cho phép bán âm
            if data.get('allow_negative'):
                self.click(self.radio_negative_allow)
            else:
                self.click(self.radio_negative_no)
        else:
            self.click(self.radio_inv_no)

    def _fill_inventory_setup_dialog(self, data):
        """Xử lý Dialog Thiết lập tồn kho cho sản phẩm (Hỗ trợ cả đơn và biến thể)"""
        dialog = self.page.locator("div[role='dialog']").filter(has_text=re.compile(r"Thiết lập tồn kho|Inventory setup", re.I))
        dialog.wait_for(state="visible", timeout=5000)
        self._log("Inventory setup dialog appeared.")

        # Lấy tất cả các dòng trong bảng (trừ dòng header)
        rows = dialog.locator("table tbody tr")
        row_count = rows.count()
        self._log(f"Found {row_count} rows in inventory table.")

        # Nếu là sản phẩm đơn (1 dòng) hoặc điền hàng loạt cho biến thể
        for i in range(row_count):
            row = rows.nth(i)
            # 1. Batch name (Cột 2)
            if 'batch_name' in data:
                batch_input = row.locator("td").nth(1).locator("input")
                self.fill_smart(batch_input, data['batch_name'])

            # 2. Expiration date (Cột 3)
            if 'expiry_date' in data:
                self._log(f"Handling expiry date for row {i + 1}: {data['expiry_date']}")
                # Bám vào Identity
                date_picker = row.locator('button[aria-haspopup="dialog"]')
                self.click(date_picker)
                
                # Parse dữ liệu mục tiêu
                day, month, year = data['expiry_date'].split('/')
                day_to_click = str(int(day))
                target_month_label = f"Tháng {int(month)}" # Format tiếng Việt phổ biến
                
                # Chờ calendar xuất hiện
                self.page.get_by_role("grid").wait_for(state="visible", timeout=3000)
                
                # --- Logic Điều hướng Tháng/Năm ---
                # Tìm nút Next và Label tháng/năm hiện tại trong Popover
                next_btn = self.page.locator("button:has(svg.lucide-chevron-right), button[name='next-month']").last
                month_year_label = self.page.locator("div[aria-live='polite'], .rdp-caption_label").last
                
                # Click 'Next' tối đa 24 lần (2 năm) để tìm đúng Tháng/Năm
                for _ in range(24):
                    current_text = month_year_label.inner_text()
                    # Nếu đã khớp cả Năm và (Tháng chữ hoặc Tháng số)
                    if year in current_text and (target_month_label in current_text or f" {int(month)} " in current_text):
                        break
                    next_btn.click()
                    self.wait(0.1) # Chờ chuyển hiệu ứng tháng
                
                # --- Chọn ngày và Xác nhận ---
                # Tìm tất cả button trong grid, lọc lấy button có đúng số ngày và KHÔNG phải ngày của tháng khác (outside)
                self._log(f"Searching for day {day_to_click} in current month grid")
                
                # Cách định vị chuẩn: Tìm button có text khớp chính xác và không bị mờ (opacity-50/muted/outside)
                day_cell = self.page.locator("button").filter(has_text=re.compile(f"^{day_to_click}$")).filter(
                    has_not=self.page.locator("[class*='outside'], [class*='muted'], [class*='opacity-50']")
                ).first
                
                if self.is_visible(day_cell, timeout=2000):
                    self.click(day_cell)
                    self._log(f"Selected day {day_to_click} by clicking.")
                else:
                    # Fallback 1: Thử tìm theo role button chuẩn
                    day_btn = self.page.get_by_role("button", name=day_to_click, exact=True).filter(visible=True).first
                    if self.is_visible(day_btn):
                        self.click(day_btn)
                    else:
                        # Fallback 2: Gõ trực tiếp
                        self._log("Still cannot click, typing date as final resort")
                        self.page.keyboard.type(data['expiry_date'])
                        self.page.keyboard.press("Enter")
                
                self.wait(0.3)
                self._log(f"Finished expiry date: {date_picker.inner_text()}")

            # 3. Total stock (Cột 4)
            if 'total_stock' in data:
                stock_input = row.locator("td").nth(3).locator("input")
                # Nếu data['total_stock'] là list (cho từng biến thể) thì lấy theo index, nếu không lấy giá trị chung
                stock_val = data['total_stock'][i] if isinstance(data['total_stock'], list) else data['total_stock']
                self.fill_smart(stock_input, str(stock_val))

        # 4. Bấm nút Add để xác nhận
        add_btn = dialog.locator("button").filter(has_text=re.compile(r"^Add$|^Thêm$|^Xác nhận$", re.I)).last
        self._log("Clicking 'Add' button to confirm inventory setup.")
        self.click(add_btn)
        
        # Chờ dialog đóng
        dialog.wait_for(state="hidden", timeout=5000)

    def _setup_variants(self, variants_config):
        """Thiết lập các thuộc tính biến thể (Màu sắc, Kích thước...)"""
        for i, config in enumerate(variants_config):
            self._log(f"Adding variant attribute: {config['attribute']}")
            
            if i > 0:
                # Bấm nút thêm dòng thuộc tính mới
                add_attr_btn = self.page.locator("button").filter(has_text=re.compile(r"Add variant attribute|Thêm thuộc tính", re.I))
                self.click(add_attr_btn)

            # Mỗi dòng thuộc tính thường nằm trong một div hoặc row
            # Ta tìm tất cả các input textbox trong vùng chứa biến thể
            variant_section = self.page.locator("div:has(> button[role='radio'][value='true'])").locator("xpath=following-sibling::div[1]")
            
            # Input tên thuộc tính: Là input đầu tiên trong mỗi dòng (row)
            attr_input = self.page.get_by_placeholder(re.compile(r"Màu sắc|Color", re.I)).nth(i)
            if not self.is_visible(attr_input, timeout=2000):
                # Dự phòng: tìm input đầu tiên của dòng thứ i trong div có class grid-cols-12
                attr_input = self.page.locator(".grid-cols-12").nth(i).locator("input[type='text']").first

            self.fill_smart(attr_input, config['attribute'])
            self.page.keyboard.press("Enter")

            # Input giá trị: Là input thứ hai trong mỗi dòng
            value_input = self.page.get_by_placeholder(re.compile(r"Đỏ, Xanh|Red, Blue", re.I)).nth(i)
            if not self.is_visible(value_input, timeout=2000):
                value_input = self.page.locator(".grid-cols-12").nth(i).locator("input[type='text']").nth(1)

            for val in config['values']:
                self.fill_smart(value_input, val)
                self.page.keyboard.press("Enter")
                self.wait(0.3)

        pass

    def _fill_variants_inventory(self, variants_config):
        pass

    @allure.step("Lưu sản phẩm")
    def save(self):
        self.click(self.save_btn.filter(visible=True).first)
        self.page.wait_for_url(re.compile(r".*/products$|.*/products/.*"), timeout=15000)
