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

        self.radio_for_sale = get_radio("For sale")
        self.radio_internal_use = get_radio("For internal use")
        self.radio_variant_no = get_radio("No")
        self.radio_variant_yes = get_radio("Yes")
        self.radio_inv_no = get_radio("No tracking")
        self.radio_inv_tracking = get_radio("Tracking")
        self.radio_negative_no = get_radio("Not allowed")
        self.radio_negative_allow = get_radio("Allow")

        # --- Locators: Buttons ---
        self.save_btn = self.page.get_by_role("button", name=re.compile(r"^Lưu$|^Save$", re.I))
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
            self.wait(1.0) 
            self._setup_variants(data.get('variants_config', []))
            # NHẬP GIÁ CHO CÁC BIẾN THỂ VỪA TẠO
            self._fill_variant_prices(data)
        else:
            self.click(self.radio_variant_no)
            if 'wholesale_price' in data: self.fill_by_label("Wholesale price", str(data['wholesale_price']))
            if 'sale_price' in data: self.fill_by_label("Sale price", str(data['sale_price']))

        # 5. Quản lý kho
        if data.get('manage_inventory'):
            self.click(self.radio_inv_tracking)
            if self.is_visible(self.enter_quantity_btn):
                self.click(self.enter_quantity_btn)
                self._fill_inventory_setup_dialog(data)
            
            if data.get('allow_negative'):
                self.click(self.radio_negative_allow)
            else:
                self.click(self.radio_negative_no)
        else:
            self.click(self.radio_inv_no)

        self.save()

    def _setup_variants(self, variants_config):
        """Thiết lập các thuộc tính biến thể: Điền dòng -> Lưu dòng -> Thêm dòng mới (nếu có)"""
        # Chờ phần biến thể render xong
        self.page.wait_for_selector("text=Attribute name", timeout=10000)
        
        for i, config in enumerate(variants_config):
            self._log(f"Process variant attribute {i+1}: {config['attribute']}")
            
            if i > 0:
                # Tìm nút 'Add another attribute' một cách linh hoạt hơn
                add_attr_selector = "button:has-text('Add another attribute'), button:has-text('Thêm thuộc tính')"
                self.wait_for_element(add_attr_selector)
                self.click(add_attr_selector)
                # Đợi dòng mới xuất hiện bằng cách kiểm tra số lượng combobox tăng lên hoặc dòng mới xuất hiện
                self.wait(1.0)

            # Container dòng hiện tại: div.space-y-3 chứa nhãn 'Attribute name'
            # Dùng .last để nhắm vào dòng vừa được thêm hoặc dòng đang hiển thị duy nhất
            current_section = self.page.locator("div.space-y-3").filter(has=self.page.locator("label", has_text=re.compile(r"Attribute name|Tên thuộc tính", re.I))).last
            current_section.scroll_into_view_if_needed()

            # 3. Chọn Tên thuộc tính
            attr_combobox = current_section.locator("button[role='combobox']").first
            self.select_from_dropdown(attr_combobox, config['attribute'])
            self.wait(0.5)

            # 4. Nhập các Giá trị
            for val in config['values']:
                self._log(f"Searching and selecting value: {val}")
                # Trong vùng hiện tại, tìm combobox để nhập giá trị
                value_trigger = current_section.locator("button[role='combobox']").filter(has_text=re.compile(r"Select value|Chọn giá trị", re.I)).last
                if not self.is_visible(value_trigger, timeout=1000):
                    # Dự phòng nếu nhãn đã thay đổi (đã chọn 1 vài giá trị)
                    value_trigger = current_section.locator("button[role='combobox']").last

                self.click(value_trigger)
                self.wait(0.3)
                self.page.keyboard.type(val, delay=50)
                self.wait(0.8) # Đợi gợi ý hiện ra
                
                # Thử click vào gợi ý nếu có, nếu không thì nhấn Enter
                suggestion = self.page.get_by_role("option").filter(has_text=re.compile(f"^{re.escape(val)}$", re.I)).first
                if not self.is_visible(suggestion, timeout=1000):
                    suggestion = self.page.get_by_role("option").first

                if self.is_visible(suggestion, timeout=1000):
                    suggestion.click()
                else:
                    self.page.keyboard.press("Enter")
                self.wait(0.5)

            # 5. LƯU DÒNG HIỆN TẠI
            save_row_btn = current_section.locator("button").filter(has_text=re.compile(r"^Save$|^Lưu$|^Add$|^Thêm$", re.I)).first
            
            self._log(f"Clicking Save for attribute row: {config['attribute']}")
            self.click(save_row_btn)
            
            # QUAN TRỌNG: Sau khi Save, đợi dòng đó được xác nhận (biến thành text hiển thị thay vì input)
            # Hoặc ít nhất là đợi một chút để UI ổn định lại nút 'Add another attribute'
            self.wait(2.0)

    def _fill_variant_prices(self, data):
        """Nhập giá sỉ, giá lẻ và upload ảnh cho từng biến thể trong bảng (Chỉ nhập dòng Child, bỏ qua Parent bị disabled)"""
        self._log("Filling prices and images for generated variants table.")
        table_selector = "table:has-text('Wholesale price'), table:has-text('Sale price'), table:has-text('Giá sỉ')"
        self.wait_for_element(table_selector)
        table = self.page.locator(table_selector)

        # Chờ ổn định
        self.wait(2.0)

        rows = table.locator("tbody tr")
        row_count = rows.count()
        self._log(f"Found {row_count} total rows (including parents) in table.")

        data_idx = 0
        for i in range(row_count):
            row = rows.nth(i)
            inputs = row.locator("input[type='text'], input[role='spinbutton'], input:not([type='checkbox']):not([type='file'])")
            
            # Bỏ qua dòng không có đủ ô nhập giá
            if inputs.count() < 2:
                continue

            wholesale_price_input = inputs.nth(-2)
            sale_price_input = inputs.last

            # CHỈ NHẬP NẾU Ô ĐÓ ENABLED (LÀ DÒNG BIẾN THỂ THỰC TẾ)
            if wholesale_price_input.is_enabled():
                self._log(f"Filling data for enabled row {i+1} (Variant index {data_idx+1})")
                
                # 1. Upload ảnh biến thể
                file_input = row.locator("input[type='file']")
                if file_input.count() > 0:
                    if 'variant_images' in data and data_idx < len(data['variant_images']):
                        file_input.set_input_files(data['variant_images'][data_idx])
                    elif 'images' in data and data['images']:
                        # Fallback: dùng ảnh đầu tiên của sản phẩm nếu không có mảng ảnh riêng
                        file_input.set_input_files(data['images'][0])

                # 2. Điền giá
                if 'wholesale_prices' in data and data_idx < len(data['wholesale_prices']):
                    self.fill_smart(wholesale_price_input, str(data['wholesale_prices'][data_idx]))
                
                if 'sale_prices' in data and data_idx < len(data['sale_prices']):
                    self.fill_smart(sale_price_input, str(data['sale_prices'][data_idx]))
                
                data_idx += 1
            else:
                self._log(f"Row {i+1} is disabled (likely a Parent row), skipping.")

    def _fill_inventory_setup_dialog(self, data):
        """Nhập Lô/Hạn dùng và Tồn kho cho từng biến thể trong hội thoại (Sử dụng DatePicker điều hướng chuẩn)"""
        dialog = self.page.locator("div[role='dialog']").filter(has_text=re.compile(r"Thiết lập tồn kho|Inventory setup", re.I))
        dialog.wait_for(state="visible", timeout=5000)
        self.wait(1.0)
        
        rows = dialog.locator("table tbody tr")
        row_count = rows.count()
        self._log(f"Found {row_count} total rows in inventory dialog.")

        data_idx = 0
        for i in range(row_count):
            row = rows.nth(i)
            # Kiểm tra ô nhập Quantity (Cột 4) để xác định dòng Child
            quantity_input = row.locator("td").nth(3).locator("input")
            
            if quantity_input.count() > 0 and quantity_input.is_enabled():
                self._log(f"Filling inventory for variant row {i+1} (Index {data_idx+1})")
                
                # 1. Batch name (Cột 2)
                if 'batch_name' in data:
                    batch_input = row.locator("td").nth(1).locator("input")
                    self.fill_smart(batch_input, data['batch_name'])

                # 2. Expiration date (Cột 3) - LOGIC DATEPICKER CHUẨN
                if 'expiry_date' in data:
                    self._log(f"Handling expiry date for row {i + 1}: {data['expiry_date']}")
                    date_picker = row.locator('button[aria-haspopup="dialog"]')
                    self.click(date_picker)

                    # Parse dữ liệu mục tiêu
                    day, month, year = data['expiry_date'].split('/')
                    day_to_click = str(int(day))
                    target_month_label = f"Tháng {int(month)}" # Format tiếng Việt

                    # Chờ calendar xuất hiện
                    self.page.get_by_role("grid").wait_for(state="visible", timeout=3000)

                    # --- Logic Điều hướng Tháng/Năm ---
                    next_btn = self.page.locator("button:has(svg.lucide-chevron-right), button[name='next-month']").last
                    month_year_label = self.page.locator("div[aria-live='polite'], .rdp-caption_label").last

                    # Click 'Next' tối đa 24 lần (2 năm) để tìm đúng Tháng/Năm
                    for _ in range(24):
                        current_text = month_year_label.inner_text()
                        if year in current_text and (target_month_label in current_text or f" {int(month)} " in current_text):
                            break
                        next_btn.click()
                        self.wait(0.1)

                    # --- Chọn ngày và Xác nhận ---
                    self._log(f"Searching for day {day_to_click} in current month grid")
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

                # 3. Total stock (Cột 4)
                if 'total_stock' in data:
                    stock_val = data['total_stock'][data_idx] if isinstance(data['total_stock'], list) else data['total_stock']
                    self.fill_smart(quantity_input, str(stock_val))
                
                data_idx += 1
            else:
                self._log(f"Inventory row {i+1} is Parent or disabled, skipping.")

        # Nhấn Xác nhận
        confirm_btn = dialog.locator("button").filter(has_text=re.compile(r"^Add$|^Thêm$|^Xác nhận$|^Save$|^Lưu$", re.I)).last
        self.click(confirm_btn)
        dialog.wait_for(state="hidden", timeout=5000)

    @allure.step("Lưu sản phẩm")
    def save(self):
        self.click(self.save_btn.filter(visible=True).first)
        self.page.wait_for_url(re.compile(r".*/products$|.*/products/.*"), timeout=15000)
