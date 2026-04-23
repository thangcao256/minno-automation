import pytest
from playwright.sync_api import Page, expect, Browser
import json
import os
import re # Thêm thư viện re để xử lý Regex
from typing import Generator, Dict
from dotenv import load_dotenv
import time

# Nạp các biến từ file .env
load_dotenv()

@pytest.fixture(scope="session")
def run_id():
    """Tạo một ID duy nhất theo thời gian (ví dụ: 2104_1530)"""
    return time.strftime("%d%m_%H%M")

@pytest.fixture(scope="session")
def test_data():
    # Xác định đường dẫn tuyệt đối tới thư mục gốc của project
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(project_root, "test_data.json")
    
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"]
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,
        "no_viewport": True
    }

@pytest.fixture(autouse=True)
def login_setup(page: Page, run_id, test_data):
    """Fixture tự động đăng nhập và chọn cửa hàng động"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")
    
    # Cửa hàng mặc định hoặc cửa hàng duy nhất của tuần này
    store_prefix = test_data['permission_test']['store_test']['name_prefix']
    dynamic_store_name = f"{store_prefix} {run_id}"
    fallback_store = os.getenv("STORE", "TC")
    
    page.goto(base_url)
    
    # ... (giữ nguyên phần login account/pass) ...
    if page.get_by_alt_text("Logo").first.is_visible():
        return

    # BƯỚC 1: Nhập Tài khoản
    try:
        account_input = page.locator("input:not([type='password'])").first
        account_input.wait_for(state="visible", timeout=10000)
        account_input.click()
        account_input.fill("")
        account_input.type(admin_user, delay=50)
        page.keyboard.press("Enter")
    except:
        pass
        
    # BƯỚC 2: Nhập Mật khẩu
    try:
        password_input = page.locator("input[type='password']")
        password_input.wait_for(state="visible", timeout=15000)
        password_input.click()
        password_input.fill("") 
        password_input.type(admin_pass, delay=50)
        page.locator("button[type='submit']").first.click()
    except:
        pass
    
    # BƯỚC 3: Chọn cửa hàng (Ưu tiên cửa hàng mới của tuần này)
    try:
        page.wait_for_url(re.compile(r".*/auth/select-stores.*"), timeout=10000)
        
        # Thử tìm cửa hàng động trước
        dynamic_store = page.locator("button").filter(has_text=dynamic_store_name)
        if dynamic_store.is_visible(timeout=3000):
            dynamic_store.click()
        else:
            # Nếu chưa có thì chọn cửa hàng mặc định (TC)
            page.locator("button").filter(has_text=fallback_store).click()
    except:
        if "select-stores" in page.url:
            page.locator("button.flex.items-center.w-full").first.click()
        
    # XÁC NHẬN VÀO DASHBOARD:
    # 1. Đợi Logo hiện lên (Bằng chứng thép)
    logo = page.get_by_alt_text("Logo").first
    logo.wait_for(state="visible", timeout=30000)
    
    # 2. Kiểm tra URL sử dụng re.compile để chấp nhận cả dashboard và dashboard-pos
    expect(page).to_have_url(re.compile(r".*dashboard.*"), timeout=10000)
    yield
