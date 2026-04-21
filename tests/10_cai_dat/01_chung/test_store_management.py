import pytest
from playwright.sync_api import Page, expect
import os
import re

@pytest.mark.order(0) # Chạy đầu tiên để các test sau có cửa hàng để chọn
def test_create_weekly_store(page: Page, test_data, run_id):
    """Tạo cửa hàng mới duy nhất cho mỗi tuần chạy"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    store_data = test_data['permission_test']['store_test']
    selectors = store_data['selectors']
    global_selectors = test_data['permission_test']['selectors']
    
    # Điều hướng đến trang quản lý cửa hàng
    page.goto(f"{base_url}/settings/branch") # Giả định URL dựa trên UI snapshot
    
    # Nhấn nút Thêm cửa hàng
    page.get_by_role("button", name="Thêm chi nhánh").click()
    
    # Nhập thông tin cửa hàng duy nhất
    unique_store_name = f"{store_data['name_prefix']} {run_id}"
    page.get_by_placeholder(selectors['name_placeholder']).fill(unique_store_name)
    page.get_by_placeholder(selectors['address_placeholder']).fill(store_data['address'])
    
    # Nhấn Lưu
    page.get_by_role(global_selectors['save_button_role'], name=global_selectors['save_button_name']).click()
    
    # Xác nhận tạo thành công
    expect(page.get_by_text(unique_store_name)).to_be_visible(timeout=10000)
