from playwright.sync_api import Page, expect
import os
import re

def test_01_login_to_minnosoft(page: Page):
    """
    [TEST CASE ĐẦU] - Quy trình Đăng nhập & Xác nhận Dashboard
    Đảm bảo hệ thống sẵn sàng và robot vào được Dashboard thành công.
    """
    # Robot sẽ tự động login qua fixture 'login_setup' trong conftest.py
    # Ở đây ta xác nhận lại trạng thái để báo PASS
    page.wait_for_url(re.compile(r".*dashboard.*"), timeout=25000, wait_until="commit")
    
    # Xác nhận Logo hệ thống
    logo = page.get_by_alt_text("Logo").first
    expect(logo).to_be_visible(timeout=15000)
    
    # Xác nhận Search bar (⌘K)
    search_box = page.locator("button").filter(has_text="⌘K").first
    expect(search_box).to_be_visible(timeout=10000)
