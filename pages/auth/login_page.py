from pages.base.base_page import BasePage
from playwright.sync_api import Page, expect
import re

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators (Cập nhật theo UI mới)
        self.username_input = "input[name='email']"
        self.password_input = "input#password"
        self.submit_button = "button[type='submit']"
        self.logo = "svg" # Logo bây giờ là SVG
        self.select_store_pattern = re.compile(r".*/auth/select-stores.*")

    def login(self, username, password):
        """Thực hiện luồng đăng nhập 2 bước của MinnoSoft"""
        # Bước 1: Username/Email
        self.fill(self.username_input, username)
        self.click(self.submit_button) # Nút 'Continue'
        
        # Bước 2: Password
        self.fill(self.password_input, password)
        self.click(self.submit_button) # Nút 'Sign in'

    def select_store(self, store_name: str):
        """
        Chọn chi nhánh (Store) dựa trên tên.
        Thực hiện cuộn xuống để tìm nếu danh sách dài và click chính xác.
        """
        print("\n🔥 [DEBUG] ĐANG CHẠY PHIÊN BẢN SELECT_STORE SIÊU CẤP - TÌM: " + str(store_name))
        if not store_name:
            self._log("⚠️ Store name is empty, skipping selection.")
            return

        self._log(f"Attempting to select store: '{store_name}'")
        self.page.wait_for_url(self.select_store_pattern, timeout=15000)
        
        # Đợi UI ổn định
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

        # Container cuộn (Thẻ div bao quanh danh sách của Radix UI)
        scroll_container = self.page.locator("div[data-radix-scroll-area-viewport]").first
        
        # Locator nhắm thẳng vào button chứa div có text là tên cửa hàng
        target_locator = self.page.locator("button").filter(
            has=self.page.locator("div.font-semibold", has_text=re.compile(f"^{re.escape(store_name)}$", re.I))
        )

        # --- VÒNG LẶP CUỘN TÌM KIẾM ---
        found = False
        for i in range(10): # Thử cuộn tối đa 10 lần
            if target_locator.count() > 0:
                found = True
                break
            
            self._log(f"Store '{store_name}' not found on current view, scrolling down (attempt {i+1})...")
            if scroll_container.count() > 0:
                # Cuộn xuống một đoạn bằng chiều cao của container
                scroll_container.evaluate("el => el.scrollTop += el.offsetHeight")
            else:
                # Dự phòng cuộn chuột toàn trang
                self.page.mouse.wheel(0, 500)
            
            self.page.wait_for_timeout(500) # Đợi danh sách render thêm

        if not found:
            all_visible = self.page.locator("div.font-semibold").all_inner_texts()
            self._log(f"❌ Store '{store_name}' NOT FOUND after scrolling. Visible: {all_visible}")
            self.take_screenshot(f"not_found_{store_name}")
            raise Exception(f"Không tìm thấy chi nhánh '{store_name}'. Đã cuộn tìm nhưng chỉ thấy: {all_visible}")

        # --- THỰC HIỆN CLICK ---
        target_button = target_locator.first
        self._log(f"Found store '{store_name}'. Scrolling to it and clicking...")
        
        # Cuộn chính xác element vào giữa vùng nhìn thấy
        target_button.evaluate("el => el.scrollIntoView({behavior: 'instant', block: 'center'})")
        self.page.wait_for_timeout(500)
        
        # Click trực tiếp
        target_button.click(force=True)
        
        # Chờ chuyển trang
        self.page.wait_for_load_state("domcontentloaded")

    def verify_login_success(self):
        """Kiểm tra login thành công bằng cách đợi Logo hiện lên"""
        expect(self.page.locator(self.logo).first).to_be_visible(timeout=30000)
        expect(self.page).to_have_url(re.compile(r".*dashboard.*"))
