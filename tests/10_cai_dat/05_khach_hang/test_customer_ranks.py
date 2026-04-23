from playwright.sync_api import Page, expect
import os
import re

def test_add_customer_rank_complete_flow(page: Page, test_data, run_id):
    """
    [TEST CASE] - Quy trình thêm Hạng khách hàng từ trang Cài đặt
    1. Vào trang settings/customer
    2. Chuyển tab sang 'Hạng khách hàng'
    3. Nhấn thêm mới và điền form
    """
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    rank_info = test_data['customer_ranks'][0]
    unique_rank_name = f"{rank_info['name']} {run_id}"
    
    # 1. Điều hướng đến trang cài đặt khách hàng
    page.goto(f"{base_url}/settings/customer")
    
    # 2. Chuyển sang Tab 'Hạng khách hàng' (Flex Language)
    # Tìm tab chứa text 'Hạng' hoặc 'Rank'
    page.locator("[role='tab'], button").filter(has_text=re.compile(r"Hạng|Rank", re.I)).click()
    page.wait_for_timeout(1000)
    
    # 3. Nhấn nút Thêm mới (Thường nằm ở phía trên bên phải của danh sách)
    # Dùng Regex để bắt nút 'Thêm' hoặc 'Add'
    add_button = page.locator("button").filter(has_text=re.compile(r"Thêm|Add", re.I)).first
    add_button.click()
    
    # 4. Điền form trong Drawer/Dialog (Index-based)
    # Thường là: Tên hạng -> Mức chi tiêu -> Giảm giá
    inputs = page.locator("input:not([type='checkbox']):not([type='radio'])")
    inputs.nth(0).fill(unique_rank_name)      # Tên hạng
    inputs.nth(1).fill(str(rank_info['min_spend'])) # Mức chi tiêu
    
    if inputs.count() > 2:
        inputs.nth(2).fill(str(rank_info['discount'])) # % Giảm giá
        
    # 5. Nhấn Lưu
    save_button = page.locator("button").filter(has_text=re.compile(r"Lưu|Save|Confirm", re.I)).first
    save_button.click()
    
    # 6. Xác nhận thành công
    # Chờ Toast hiển thị hoặc Drawer đóng lại
    expect(page.get_by_text(unique_rank_name).first).to_be_visible(timeout=10000)

def test_add_customer_tag(page: Page, run_id):
    """
    [TEST CASE] - Thêm Nhóm (Tag) khách hàng mới
    Mục này thường nằm ở tab đầu tiên mặc định.
    """
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    tag_name = f"Nhóm VIP {run_id}"
    
    page.goto(f"{base_url}/settings/customer?tab=tag")
    
    # Nhấn Thêm mới
    page.locator("button").filter(has_text=re.compile(r"Thêm|Add", re.I)).first.click()
    
    # Nhập tên nhóm (Input đầu tiên trong popup/drawer)
    page.locator("input").first.fill(tag_name)
    
    # Nhấn Lưu
    page.locator("button").filter(has_text=re.compile(r"Lưu|Save|Confirm", re.I)).first.click()
    
    # Xác nhận
    expect(page.get_by_text(tag_name).first).to_be_visible(timeout=10000)
