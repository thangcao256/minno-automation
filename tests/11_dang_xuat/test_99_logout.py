from playwright.sync_api import Page, expect
import os
import re

def test_99_logout_functionality(page: Page):
    """
    [TEST CASE CUỐI] - Quy trình Đăng xuất hoàn chỉnh
    Đảm bảo robot có thể thoát khỏi hệ thống và xóa sạch phiên làm việc.
    """
    # 1. Đảm bảo đang ở Dashboard
    page.wait_for_url(re.compile(r".*dashboard.*"), timeout=15000, wait_until="commit")
    
    # 2. Click vào Avatar người dùng (nút button cuối cùng trong header)
    avatar_button = page.locator("header button").last
    avatar_button.wait_for(state="visible", timeout=10000)
    avatar_button.click()
    
    # 3. Chọn nút Đăng xuất (Selector linh hoạt bao phủ mọi ngôn ngữ)
    logout_item = page.locator("[role='menuitem'], a[href*='logout'], button:has-text('Logout'), button:has-text('Đăng xuất')").last
    logout_item.wait_for(state="visible", timeout=5000)
    logout_item.click()
    
    # 4. Xác nhận đã quay về màn hình đăng nhập
    page.wait_for_url(re.compile(r".*/login|.*/auth/get-started"), timeout=15000)
    
    # 5. Kiểm tra sự hiện diện của ô nhập tài khoản để chốt kết quả PASS
    account_input = page.locator("input:not([type='password'])").first
    expect(account_input).to_be_visible(timeout=10000)
