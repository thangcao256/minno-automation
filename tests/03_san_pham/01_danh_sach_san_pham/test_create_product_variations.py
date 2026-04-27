import allure
import pytest
from playwright.sync_api import Page, expect
from pages.products.product_create_page import ProductCreatePage
from test_data.product_data import PRODUCT_TEST_DATA
import os
import re

@allure.epic("Sản phẩm")
@allure.feature("Thêm mới sản phẩm")
class TestCreateProduct:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Điều hướng đến trang thêm mới sản phẩm"""
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        page.goto(f"{base_url}/products/new")
        self.product_page = ProductCreatePage(page)

    @allure.title("Thêm sản phẩm đơn giản (Basic)")
    def test_create_basic_product(self, page: Page):
        data = PRODUCT_TEST_DATA["basic_product"]
        self.product_page.fill_product_data(data)

    @allure.title("Thêm sản phẩm có quản lý kho (Inventory Tracking)")
    def test_create_inventory_product(self, page: Page):
        data = PRODUCT_TEST_DATA["inventory_product"]
        self.product_page.fill_product_data(data)

    @allure.title("Thêm sản phẩm có Lô/Hạn dùng (Batch & Expiry)")
    def test_create_batch_expiry_product(self, page: Page):
        data = PRODUCT_TEST_DATA["batch_expiry_product"]
        self.product_page.fill_product_data(data)

    @allure.title("Thêm sản phẩm có biến thể (Variants)")
    def test_create_variants_product(self, page: Page):
        data = PRODUCT_TEST_DATA["variants_product"]
        self.product_page.fill_product_data(data)
