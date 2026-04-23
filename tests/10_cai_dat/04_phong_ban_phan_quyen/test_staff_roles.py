from playwright.sync_api import Page, expect
import os
import re

def test_create_role_robust(page: Page, test_data, run_id):
    """
    [TEST CASE: SETTINGS-01] - Tạo nhóm quyền (Vai trò) mới
    Chiến thuật: Sử dụng DOM Index và Type thay vì Placeholder/Text để hỗ trợ đa ngôn ngữ.
    """
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    role_info = test_data['permission_test']['roles'][0] 
    unique_role_name = f"{role_info['name']} {run_id}"
    
    page.goto(f"{base_url}/settings/role/new")
    
    # 1. Nhập tên vai trò: Là input đầu tiên trong phần nội dung chính (không nằm trong header)
    # Ta sử dụng CSS selector để bắt input trong phần main/dialog
    role_input = page.locator("main input, [role='dialog'] input, .vaul-drawer input").first
    role_input.wait_for(state="visible", timeout=10000)
    role_input.fill(unique_role_name)
    
    # 2. Chọn các quyền: Click vào các thẻ chứa text quyền
    for perm in role_info['permissions_to_select']:
        # Tìm phần tử theo text một cách linh hoạt
        page.locator(f"text='{perm}'").first.click()
    
    # 3. Nút Lưu: Sử dụng type='submit' hoặc tìm button có text "Lưu/Save" qua Regex
    save_button = page.locator("button[type='submit']")
    if not save_button.is_visible():
        save_button = page.locator("button").filter(has_text=re.compile(r"Lưu|Save|Confirm", re.I)).first
        
    save_button.click()
    
    # 4. Xác nhận quay về danh sách
    page.wait_for_url(re.compile(r".*/settings/user/role.*"), timeout=15000)
    expect(page.get_by_text(unique_role_name)).to_be_visible(timeout=10000)

def test_add_staff_robust(page: Page, test_data, run_id):
    """
    [TEST CASE: SETTINGS-02] - Thêm nhân viên mới
    Chiến thuật: Sử dụng Input Index để nhập thông tin Tên, SĐT, Email (bỏ qua placeholder).
    """
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    user_info = test_data['permission_test']['users'][0]
    role_info = test_data['permission_test']['roles'][0]
    
    unique_name = f"{user_info['full_name']} {run_id}"
    unique_email = user_info['email'].replace("@", f"_{run_id}@")
    unique_role_name = f"{role_info['name']} {run_id}"
    
    page.goto(f"{base_url}/settings/users/new")
    
    # 1. Nhập thông tin theo thứ tự các ô input trong form (thường là Tên -> SĐT -> Email)
    # Loại trừ các input không liên quan như checkbox hay radio
    inputs = page.locator("main input:not([type='checkbox']):not([type='radio'])")
    inputs.nth(0).fill(unique_name)  # Họ và tên
    inputs.nth(1).fill(user_info['phone']) # Số điện thoại
    inputs.nth(2).fill(unique_email) # Email
    
    # 2. Chọn vai trò (ComboBox)
    # Click vào combobox đầu tiên tìm thấy trong form
    page.locator("[role='combobox'], .select-trigger").first.click()
    
    # Tìm vai trò trong danh sách hiện lên
    page.get_by_text(unique_role_name).first.click()
    
    # 3. Nhấn Lưu
    save_button = page.locator("button").filter(has_text=re.compile(r"Lưu|Save|Add", re.I)).first
    save_button.click()
    
    # 4. Xác nhận
    page.wait_for_url(re.compile(r".*/settings/users.*"), timeout=15000)
    expect(page.get_by_text(unique_name)).to_be_visible(timeout=10000)
