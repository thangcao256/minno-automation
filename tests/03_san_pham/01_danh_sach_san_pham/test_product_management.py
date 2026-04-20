from playwright.sync_api import Page, expect

def test_add_product(page: Page, test_data):
    """Test case: Thêm sản phẩm mới hoàn chỉnh"""
    product = test_data['products'][0]
    page.goto("https://demo.minno.vn/dashboard/products/create")
    
    # UI snapshot: Trang Product_ Dashboard hỗ trợ nhập thông tin cơ bản
    page.get_by_placeholder("Nhập tên sản phẩm").fill(product['name'] + " (Python E2E)")
    page.locator('input[name="sku"]').fill(product['sku'] + "_AUTO")
    page.locator('input[name="basePrice"]').fill(str(product['price']))
    
    # Nhấn Lưu sản phẩm
    page.get_by_role("button", name="Lưu sản phẩm").click()
    
    # Sau khi lưu thành công, hệ thống chuyển về trang danh sách
    expect(page).to_have_url(r".*/dashboard/products")
