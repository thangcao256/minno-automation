from playwright.sync_api import Page, expect

def test_add_category(page: Page):
    """Test case: Thêm danh mục sản phẩm mới"""
    page.goto("https://demo.minno.vn/dashboard/products/categories")
    
    # UI snapshot trang Product_Category cho thấy nút "Thêm mới"
    page.get_by_role("button", name="Thêm mới").click()
    
    # Nhập tên danh mục (Locator input name="categoryName")
    page.locator('input[name="categoryName"]').fill("Điện tử & Gia dụng")
    
    # Nhấn Xác nhận/Lưu
    page.get_by_role("button", name="Lưu").click()
    expect(page.get_by_text("Thành công")).to_be_visible()

def test_add_supplier(page: Page):
    """Test case: Thêm nhà cung cấp mới"""
    page.goto("https://demo.minno.vn/dashboard/products/suppliers")
    page.get_by_placeholder("Tên nhà cung cấp").fill("NCC Linh kiện Minno")
    page.get_by_role("button", name="Lưu").click()
    expect(page.get_by_text("Thêm nhà cung cấp thành công")).to_be_visible()

def test_add_attribute(page: Page):
    """Test case: Thêm thuộc tính sản phẩm (Màu sắc/Kích thước)"""
    page.goto("https://demo.minno.vn/dashboard/products/attributes")
    page.get_by_placeholder("Tên thuộc tính").fill("Chất liệu")
    page.get_by_role("button", name="Thêm").click()
    expect(page.get_by_text("Đã thêm thuộc tính")).to_be_visible()
