from pages.products.product_page import ProductPage
from playwright.sync_api import Page
import os

def test_add_product_category_pom(page: Page, test_data, run_id):
    """[TC-PROD-01]: Thêm Danh mục sản phẩm sử dụng POM"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    category = test_data['catalog_test']['categories'][0]
    unique_name = f"{category['name']} {run_id}"
    
    # Điều hướng
    page.goto(f"{base_url}/product/category?tab=category")
    
    # Thực hiện action qua Page Object
    product_page = ProductPage(page)
    product_page.add_category(name=unique_name)

def test_add_product_attribute_pom(page: Page, test_data, run_id):
    """[TC-PROD-02]: Thêm Thuộc tính sản phẩm sử dụng POM"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    attribute = test_data['catalog_test']['attributes'][0]
    unique_name = f"{attribute['name']} {run_id}"
    
    page.goto(f"{base_url}/product/category?tab=attribute")
    
    product_page = ProductPage(page)
    product_page.add_attribute(attr_name=unique_name, values=attribute['values'])
