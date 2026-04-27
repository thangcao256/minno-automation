import pytest
import allure
from pages.products.product_create_page import ProductCreatePage
from pages.products.product_list_page import ProductListPage
from test_data.product_data import PRODUCT_MATRIX_DATA
import os

@allure.feature("Quản lý sản phẩm")
@allure.story("Tạo và Xác nhận sản phẩm")
class TestCreateAndVerifyProduct:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.product_create_page = ProductCreatePage(page)
        self.product_list_page = ProductListPage(page)
        self.base_url = os.getenv("BASE_URL", "https://demo.minno.vn")

    @allure.title("Tạo sản phẩm đơn và xác nhận trong danh sách")
    def test_create_simple_product_and_verify(self, page):
        # 1. Lấy dữ liệu mẫu (Sản phẩm đơn, có quản lý kho)
        data = PRODUCT_MATRIX_DATA["S1_V1_I2_N1"]
        
        # 2. Điều hướng tới trang tạo sản phẩm
        self.product_create_page.navigate(f"{self.base_url}/products/new")
        
        # 3. Điền thông tin và lưu
        self.product_create_page.fill_product_data(data)
        # Hàm fill_product_data của bạn đã gọi self.save() ở cuối
        
        # 4. Quay lại trang danh sách (nếu save() chưa redirect)
        self.product_list_page.navigate(f"{self.base_url}/products")
        
        # 5. Tìm kiếm và Verify
        self.product_list_page.search(data['name'])
        self.product_list_page.verify_product_in_list(
            name=data['name'],
            sku=data.get('SKU'),
            price=str(data.get('sale_price')),
            stock=str(data.get('total_stock'))
        )

    @allure.title("Tạo sản phẩm biến thể và xác nhận")
    def test_create_variant_product_and_verify(self, page):
        # 1. Lấy dữ liệu mẫu (Sản phẩm có 4 biến thể)
        data = PRODUCT_MATRIX_DATA["S1_V2_I2_N1"]
        
        # 2. Điều hướng tới trang tạo sản phẩm
        self.product_create_page.navigate(f"{self.base_url}/products/new")
        
        # 3. Điền thông tin (bao gồm biến thể và tồn kho từng dòng)
        self.product_create_page.fill_product_data(data)

        # 4. Quay lại trang danh sách
        self.product_list_page.navigate(f"{self.base_url}/products")
        
        # 5. Tìm kiếm theo tên cha
        self.product_list_page.search(data['name'])
        
        # 6. Verify sản phẩm cha hiển thị tổng tồn kho
        total_stock = sum(data['total_stock']) if isinstance(data['total_stock'], list) else data['total_stock']
        self.product_list_page.verify_product_in_list(
            name=data['name'],
            sku=data.get('SKU'),
            stock=str(total_stock)
        )
