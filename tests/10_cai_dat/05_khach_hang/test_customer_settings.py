from playwright.sync_api import Page, expect
import os
import re

def test_add_customer_tag_robust(page: Page, run_id):
    """
    [TEST CASE] - Thêm Thẻ (Tag) khách hàng mới
    Sử dụng URL trực tiếp, XPath tương đối và button type='submit'
    """
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    unique_tag_name = f"Thẻ VIP {run_id}"
    
    # 1. Nhảy thẳng vào tab Thẻ
    page.goto(f"{base_url}/settings/customer?tab=tag")
    
    # 2. Click nút Thêm (Dùng XPath tương đối để ổn định)
    add_button = page.locator('//*[@id="radix-_r_13_"]/div/div[2]/div[2]/div/div/div/div/div[3]/div[1]/div[2]/button').first
    add_button.wait_for(state="visible", timeout=10000)
    add_button.click()
    
    # 3. Nhập tên thẻ (Input đầu tiên trong Drawer)
    tag_input = page.locator("input").first
    tag_input.wait_for(state="visible", timeout=10000)
    tag_input.fill(unique_tag_name)
    
    # 4. Nhấn Lưu (Dùng type='submit' cực chuẩn)
    save_button = page.locator('button[type="submit"]').first
    save_button.click()
    
    # 5. Xác nhận thành công
    expect(page.get_by_text(unique_tag_name).first).to_be_visible(timeout=10000)

def test_add_customer_group_robust(page: Page, run_id):
    """
    [TEST CASE] - Thêm Nhóm khách hàng mới
    Sử dụng URL trực tiếp, XPath tương đối và button type='submit'
    """
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    unique_group_name = f"Nhóm E2E {run_id}"
    
    # 1. Nhảy thẳng vào tab Nhóm khách hàng
    page.goto(f"{base_url}/settings/customer?tab=customer_group")
    
    # 2. Click nút Thêm
    add_button = page.locator('//*[@id="radix-_r_13_"]/div/div[2]/div[2]/div/div/div/div/div[3]/div[1]/div[2]/button').first
    add_button.wait_for(state="visible", timeout=10000)
    add_button.click()
    
    # 3. Nhập tên nhóm
    group_input = page.locator("input").first
    group_input.wait_for(state="visible", timeout=10000)
    group_input.fill(unique_group_name)
    
    # 4. Nhấn Lưu (type='submit')
    save_button = page.locator('button[type="submit"]').first
    save_button.click()
    
    # 5. Xác nhận thành công
    expect(page.get_by_text(unique_group_name).first).to_be_visible(timeout=10000)
