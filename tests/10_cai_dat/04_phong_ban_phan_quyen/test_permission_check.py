import pytest
from playwright.sync_api import Page, expect
import os
import re

@pytest.fixture
def permission_data(test_data):
    return test_data['permission_test']

@pytest.mark.order(1)
def test_create_roles_from_json(page: Page, permission_data, run_id):
    """Tạo vai trò với tên duy nhất (Unique Name)"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    selectors = permission_data['selectors']
    
    for role in permission_data['roles']:
        page.goto(f"{base_url}/settings/role/new")
        
        # Thêm run_id vào tên để tránh trùng lặp
        unique_role_name = f"{role['name']} {run_id}"
        page.get_by_placeholder(selectors['role_name_placeholder']).fill(unique_role_name)
        
        for perm in role['permissions_to_select']:
            page.get_by_text(perm).first.click()
            
        page.get_by_role(selectors['save_button_role'], name=selectors['save_button_name']).click()
        page.wait_for_url(re.compile(r".*/settings/user/role.*"))

@pytest.mark.order(2)
def test_create_users_from_json(page: Page, permission_data, run_id):
    """Tạo người dùng với email duy nhất (Unique Email)"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    selectors = permission_data['selectors']
    
    for user_info in permission_data['users']:
        page.goto(f"{base_url}/settings/users/new")
        
        # Thêm run_id vào tên và email
        unique_name = f"{user_info['full_name']} {run_id}"
        unique_email = user_info['email'].replace("@", f"_{run_id}@")
        
        page.get_by_placeholder(selectors['staff_name_placeholder']).fill(unique_name)
        page.get_by_placeholder(selectors['staff_phone_placeholder']).fill(user_info['phone'])
        page.get_by_placeholder(selectors['staff_email_placeholder']).fill(unique_email)
        
        # Tìm đúng tên vai trò đã tạo ở bước 1 (có kèm run_id)
        role_name_base = next(r['name'] for r in permission_data['roles'] if r['key'] == user_info['role_key'])
        unique_role_name = f"{role_name_base} {run_id}"
        
        page.get_by_role("combobox").click()
        page.get_by_text(unique_role_name).click()
        
        page.get_by_role(selectors['save_button_role'], name=selectors['save_button_name']).click()
        page.wait_for_timeout(2000)

@pytest.mark.order(3)
def test_verify_permissions_dynamic(browser, permission_data, run_id):
    """Kiểm tra phân quyền động (Verify Sidebar)"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    
    for user_info in permission_data['users']:
        context = browser.new_context()
        page = context.new_page()
        page.goto(base_url)
        
        role_data = next(r for r in permission_data['roles'] if r['key'] == user_info['role_key'])
        
        # Kiểm tra Menu Sidebar
        for menu in role_data['visible_menus']:
            expect(page.get_by_role("link", name=menu)).to_be_visible()
            
        for menu in role_data['hidden_menus']:
            expect(page.get_by_role("link", name=menu)).not_to_be_visible()
            
        context.close()
