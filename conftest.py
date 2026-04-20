import pytest
from playwright.sync_api import Page, expect, Browser
import json
import os
import re # Thêm thư viện re để xử lý Regex
from typing import Generator, Dict
from dotenv import load_dotenv

# Nạp các biến từ file .env
load_dotenv()

@pytest.fixture(scope="session")
def test_data():
    with open("test_data.json", encoding="utf-8") as f:
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
    }

@pytest.fixture(autouse=True)
def login_setup(page: Page):
    """Fixture tự động đăng nhập và chọn đúng cửa hàng dựa trên UI thực tế"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")
    store_name = os.getenv("STORE", "TC")
    
    page.goto(base_url)
    
    # Nếu Logo đã hiện ra thì coi như đã đăng nhập
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
    
    # BƯỚC 3: Chọn cửa hàng
    try:
        page.wait_for_url(re.compile(r".*/auth/select-stores.*"), timeout=10000, wait_until="commit")
        store_selector = page.locator("button").filter(has_text=store_name)
        store_selector.wait_for(state="visible", timeout=10000)
        store_selector.click()
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
