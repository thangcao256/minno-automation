import allure
from playwright.sync_api import Page, expect
from pages.products.product_create_page import ProductCreatePage
import os
import re

@allure.epic("Products")
@allure.feature("Product Management")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_product_full_flow(page: Page, test_data, run_id):
    """
    Test case: Thêm sản phẩm mới hoàn chỉnh (Full Flow)
    Sử dụng Page Object Model hoàn thiện và dữ liệu chuẩn API từ test_data.json
    """
    # 1. Chuẩn bị dữ liệu duy nhất
    product_data = test_data['products'][0].copy()
    product_data['name'] = f"{product_data['name']} {run_id}"
    product_data['SKU_code'] = f"{product_data['SKU_code']}_{run_id}"
    
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    
    # 2. Đi tới trang tạo sản phẩm
    page.goto(f"{base_url}/products/new")
    
    product_create = ProductCreatePage(page)
    
    # 3. Nhập thông tin đầy đủ theo logic API
    product_create.fill_product_data(product_data)
    
    # 4. Lưu sản phẩm
    product_create.save()
    
    # 5. Xác nhận đã quay về danh sách
    expect(page).to_have_url(re.compile(r".*/products$"))
