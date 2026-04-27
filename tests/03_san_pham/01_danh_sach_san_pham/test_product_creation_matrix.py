import allure
import pytest
from playwright.sync_api import Page
from pages.products.product_create_page import ProductCreatePage
from test_data.product_data import PRODUCT_MATRIX_DATA
import os

@allure.epic("Sản phẩm")
@allure.feature("Thêm mới sản phẩm (Matrix Coverage)")
class TestProductCreationMatrix:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Điều hướng đến trang thêm mới sản phẩm trước mỗi test case"""
        base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
        page.goto(f"{base_url}/products/new")
        self.product_page = ProductCreatePage(page)

    @pytest.mark.parametrize("case_id", PRODUCT_MATRIX_DATA.keys())
    def test_create_product_matrix(self, page: Page, case_id):
        """
        [E2E-MATRIX]: Kiểm thử bao phủ toàn bộ ma trận sản phẩm.
        - Sale vs Internal
        - Simple vs Variants
        - Inventory vs No Inventory
        - Allow vs Not Allow Negative
        """
        data = PRODUCT_MATRIX_DATA[case_id]
        allure.dynamic.title(f"Case {case_id}: {data['name']}")
        
        with allure.step(f"Điền dữ liệu cho case {case_id}"):
            self.product_page.fill_product_data(data)
            
        with allure.step("Lưu sản phẩm và xác nhận thành công"):
            self.product_page.save()
            # Ở đây có thể thêm assertion kiểm tra sản phẩm hiển thị trong danh sách nếu cần
