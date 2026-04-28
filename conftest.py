import pytest
from playwright.sync_api import Page, expect
import json
import os
import re
from dotenv import load_dotenv
import time
from pages.auth.login_page import LoginPage
from pages.dashboard.dashboard_page import DashboardPage

# Nạp các biến từ file .env
load_dotenv()

def pytest_runtest_setup(item):
    """In tên test case ra terminal trước khi bắt đầu chạy"""
    print(f"\n🚀 STARTING TEST: {item.nodeid}")

@pytest.fixture(scope="session")
def run_id():
    """Tạo một ID duy nhất theo thời gian"""
    return time.strftime("%d%m_%H%M")

@pytest.fixture(scope="session")
def test_data():
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(project_root, "test_data", "test_data.json")
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--start-maximized"]}

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": None, "no_viewport": True}

@pytest.fixture(autouse=True)
def login_setup(page: Page, run_id, test_data):
    """Fixture tự động đăng nhập và tự động đăng xuất (Teardown)"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")
    fallback_store = os.getenv("STORE", "TC")
    
    login_page = LoginPage(page)
    dashboard = DashboardPage(page)
    
    # 1. Mở trang chủ
    login_page.navigate(base_url)
    
    # 2. Thực hiện Login (nếu chưa login)
    if not dashboard.is_visible(dashboard.user_menu_avatar, timeout=3000):
        login_page.login(admin_user, admin_pass)
        try:
            login_page.select_store(fallback_store)
        except:
            pass
        login_page.verify_login_success()
    
    yield # <--- TEST CASE CHẠY TẠI ĐÂY
    
    # 3. TEARDOWN: Tự động Đăng xuất
    # Ta kiểm tra xem Avatar có hiển thị không (bất kể đang ở URL nào)
    if dashboard.is_visible(dashboard.user_menu_avatar, timeout=2000):
        dashboard.logger.info("Test finished. Executing automatic logout...")
        dashboard.logout()
        # Chờ 1 giây để người dùng kịp nhìn thấy kết quả đăng xuất
        page.wait_for_timeout(1000)
