import pytest
import allure
import os
import re
from playwright.sync_api import Page, expect
from pages.products.product_create_page import ProductCreatePage
from pages.products.product_list_page import ProductListPage
from test_data.product_data import PRODUCT_MATRIX_DATA, DEFAULT_IMAGE, run_id

@allure.epic("Sản phẩm")
@allure.feature("Quản lý sản phẩm")
class TestProductCreationCoverage:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.product_create_page = ProductCreatePage(page)
        self.product_list_page = ProductListPage(page)
        self.base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        
    @allure.story("Tạo sản phẩm Coverage")
    @allure.title("P01: Tạo sản phẩm Dịch vụ (For Sale, No Inventory, No Variants)")
    def test_p01_create_service_product(self, page: Page):
        data = PRODUCT_MATRIX_DATA["S1_V1_I1"]
        
        with allure.step("1. Điều hướng tới trang tạo sản phẩm"):
            page.goto(f"{self.base_url}/products/new")
        
        with allure.step("2. Nhập thông tin và lưu"):
            self.product_create_page.fill_product_data(data)
            
        with allure.step("3. Xác nhận sản phẩm trong danh sách"):
            # Chờ quay về danh sách
            self.product_list_page.search(data['name'])
            self.product_list_page.verify_product_in_list(
                name=data['name'],
                price=str(data['sale_price'])
            )

    @allure.story("Tạo sản phẩm Coverage")
    @allure.title("P02: Tạo sản phẩm Kho Chuẩn (For Sale, Tracking, No Negative, Batch/Expiry)")
    def test_p02_create_standard_inventory_product(self, page: Page):
        # Dữ liệu sản phẩm đơn có quản lý kho, không cho phép âm
        data = {
            "name": f"SP Kho Chuẩn P02 {run_id}",
            "SKU": f"SKU-P02-{run_id}",
            "for_sale": True,
            "has_variants": False,
            "manage_inventory": True,
            "allow_negative": False, # Theo yêu cầu của user
            "batch_name": f"BATCH-P02-{run_id}",
            "expiry_date": "20/12/2026",
            "total_stock": 100,
            "sale_price": 150000,
            "category": "Danh mục 2504_0841",
            "images": [DEFAULT_IMAGE]
        }
        
        with allure.step("1. Điều hướng tới trang tạo sản phẩm"):
            page.goto(f"{self.base_url}/products/new")
            
        with allure.step("2. Nhập thông tin và lưu"):
            self.product_create_page.fill_product_data(data)
            
        with allure.step("3. Xác nhận sản phẩm và tồn kho"):
            self.product_list_page.search(data['name'])
            self.product_list_page.verify_product_in_list(
                name=data['name'],
                stock=str(data['total_stock'])
            )

    @allure.story("Tạo sản phẩm Coverage")
    @allure.title("P03: Tạo sản phẩm Nội bộ (Internal Use, Tracking, Allow Negative)")
    def test_p03_create_internal_negative_product(self, page: Page):
        data = PRODUCT_MATRIX_DATA["S2_V1_I2_N2"]
        
        with allure.step("1. Điều hướng tới trang tạo sản phẩm"):
            page.goto(f"{self.base_url}/products/new")
            
        with allure.step("2. Nhập thông tin và lưu"):
            self.product_create_page.fill_product_data(data)
            
        with allure.step("3. Xác nhận sản phẩm nội bộ"):
            self.product_list_page.search(data['name'])
            self.product_list_page.verify_product_in_list(name=data['name'])
            # Nội bộ thường không hiển thị giá bán lẻ (hoặc bằng 0)
            
    @allure.story("Tạo sản phẩm Coverage")
    @allure.title("P04: Tạo sản phẩm Biến thể đầy đủ (Full Variants, Tracking, No Negative, Batch/Expiry)")
    def test_p04_create_full_variant_product(self, page: Page):
        # Dùng dữ liệu S1_V2_I2_N1 nhưng đổi allow_negative sang False
        data = PRODUCT_MATRIX_DATA["S1_V2_I2_N1"].copy()
        data["name"] = f"SP Biến Thể Full P04 {run_id}"
        data["SKU"] = f"SKU-P04-{run_id}"
        data["allow_negative"] = False # Chặn bán âm theo yêu cầu
        
        with allure.step("1. Điều hướng tới trang tạo sản phẩm"):
            page.goto(f"{self.base_url}/products/new")
            
        with allure.step("2. Nhập thông tin biến thể, giá và tồn kho"):
            # fill_product_data sẽ tự động gọi _setup_variants, _fill_variant_prices và _fill_inventory_setup_dialog
            self.product_create_page.fill_product_data(data)
            
        with allure.step("3. Xác nhận sản phẩm cha và tổng tồn kho"):
            self.product_list_page.search(data['name'])
            total_stock = sum(data['total_stock']) if isinstance(data['total_stock'], list) else data['total_stock']
            self.product_list_page.verify_product_in_list(
                name=data['name'],
                stock=str(total_stock)
            )

    @allure.story("Tạo sản phẩm Coverage")
    @allure.title("P05: Tạo sản phẩm Biến thể Dịch vụ (Variants, No Inventory)")
    def test_p05_create_variant_service_product(self, page: Page):
        data = PRODUCT_MATRIX_DATA["S1_V2_I1"]
        
        with allure.step("1. Điều hướng tới trang tạo sản phẩm"):
            page.goto(f"{self.base_url}/products/new")
            
        with allure.step("2. Nhập thông tin biến thể không quản lý kho"):
            self.product_create_page.fill_product_data(data)
            
        with allure.step("3. Xác nhận trong danh sách"):
            self.product_list_page.search(data['name'])
            self.product_list_page.verify_product_in_list(name=data['name'])
