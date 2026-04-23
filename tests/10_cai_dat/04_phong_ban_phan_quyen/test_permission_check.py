import pytest
from playwright.sync_api import Page, expect
import os
import re

@pytest.fixture
def permission_data(test_data):
    return test_data['permission_test']

# MAPPING INDEX CỐ ĐỊNH (FIXED ORDER STRATEGY)
# Quy định thứ tự các hạng mục quyền từ trên xuống dưới để chống trượt do ngôn ngữ
PERMISSION_ORDER = {
    "Sản phẩm": 0,
    "Tồn kho": 1,
    "Đơn hàng": 2,
    "Bán hàng (POS)": 3,
    "Khách hàng": 4,
    "Tài chính": 5,
    "Cài đặt": 6
}

@pytest.mark.order(1)
def test_create_roles_from_json(page: Page, permission_data, run_id):
    """Tạo vai trò bằng cách bắt theo số thứ tự (Index) các mục"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    
    for role in permission_data['roles']:
        page.goto(f"{base_url}/settings/role/new")
        
        # 1. Nhập tên vai trò (Robust selector)
        role_input = page.locator("main input, [role='dialog'] input").first
        role_input.wait_for(state="visible", timeout=15000)
        
        unique_role_name = f"{role['name']} {run_id}"
        role_input.fill(unique_role_name)
        
        # 2. Chọn các quyền theo Index (Quy định thứ tự)
        # Tìm tất cả các dòng chứa checkbox trong danh sách quyền
        # UI MinnoSoft thường dùng thẻ label bọc checkbox hoặc các div có role='checkbox'
        checkboxes = page.locator("main [role='checkbox'], main label:has(button[role='checkbox']), main tr:has(button)")
        
        for perm_key in role['permissions_to_select']:
            if perm_key in PERMISSION_ORDER:
                idx = PERMISSION_ORDER[perm_key]
                print(f"Đang tick quyền: {perm_key} (Index: {idx})")
                
                # Bắt theo index nth(idx)
                target = checkboxes.nth(idx)
                if target.is_visible():
                    target.click()
                    page.wait_for_timeout(200) # Nghỉ ngắn giữa các lần click
            
        # 3. Nút Lưu (Flex Language - Dùng Regex để an toàn)
        save_button = page.locator("button").filter(has_text=re.compile(r"^Lưu$|^Save$|^Confirm$|^Create$", re.I)).first
        save_button.click()
        
        # Chờ chuyển hướng
        page.wait_for_url(re.compile(r".*/settings/user/role.*"), timeout=15000)
        expect(page.get_by_text(unique_role_name)).to_be_visible(timeout=10000)

@pytest.mark.order(2)
def test_create_users_from_json(page: Page, permission_data, run_id):
    """Tạo người dùng với Input Index"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    
    for user_info in permission_data['users']:
        page.goto(f"{base_url}/settings/users/new")
        
        unique_name = f"{user_info['full_name']} {run_id}"
        unique_email = user_info['email'].replace("@", f"_{run_id}@")
        
        # Nhập thông tin (Tên -> SĐT -> Email)
        inputs = page.locator("main input:not([type='checkbox']):not([type='radio'])")
        inputs.nth(0).fill(unique_name)
        inputs.nth(1).fill(user_info['phone'])
        inputs.nth(2).fill(unique_email)
        
        # Chọn vai trò
        role_name_base = next(r['name'] for r in permission_data['roles'] if r['key'] == user_info['role_key'])
        unique_role_name = f"{role_name_base} {run_id}"
        
        page.locator("[role='combobox'], .select-trigger").first.click()
        page.get_by_text(unique_role_name).first.click()
        
        # Lưu
        save_button = page.locator("button").filter(has_text=re.compile(r"Lưu|Save|Add|Confirm", re.I)).first
        save_button.click()
        
        page.wait_for_timeout(2000)
