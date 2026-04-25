import allure
import pytest
from pages.products.product_page import ProductPage
from playwright.sync_api import Page

@allure.feature("Cài đặt sản phẩm")
@allure.story("Quản lý Danh mục, Nhóm, Nguồn hàng và Thuộc tính")
class TestProductSettings:
    
    def test_add_product_category(self, page: Page, test_data, run_id):
        """[TC-PROD-01]: Thêm Danh mục sản phẩm"""
        unique_name = f"Danh mục {run_id}"
        prod_page = ProductPage(page)
        prod_page.navigate_to_category_tab("category")
        prod_page.add_category(name=unique_name, code=f"CAT_{run_id}")

    def test_add_product_group(self, page: Page, test_data, run_id):
        """[TC-PROD-02]: Thêm Nhóm sản phẩm"""
        unique_name = f"Nhóm {run_id}"
        prod_page = ProductPage(page)
        prod_page.navigate_to_category_tab("group")
        prod_page.add_group(name=unique_name, code=f"GRP_{run_id}")

    def test_add_product_attribute(self, page: Page, test_data, run_id):
        """[TC-PROD-04]: Thêm Thuộc tính sản phẩm"""
        attr_data = test_data['catalog_test']['attributes'][0]
        unique_name = f"{attr_data['name']} {run_id}"
        prod_page = ProductPage(page)
        prod_page.navigate_to_category_tab("attribute")
        prod_page.add_attribute(attr_name=unique_name, values=attr_data['values'])

    def test_add_product_supplier(self, page: Page, test_data, run_id):
        """[TC-PROD-03]: Thêm Nhà cung cấp (Nguồn hàng)"""
        unique_name = f"Nguồn hàng {run_id}"
        prod_page = ProductPage(page)
        prod_page.navigate_to_category_tab("supplier")
        prod_page.add_supplier(name=unique_name)
        page.keyboard.press("Escape")