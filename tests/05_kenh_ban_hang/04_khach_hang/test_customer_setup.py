from playwright.sync_api import Page, expect

def test_add_customer_tag(page: Page):
    """Test case: Thêm thẻ (Tag) khách hàng"""
    # UI snapshot trang settings-customer cho thấy menu Thẻ khách hàng
    page.goto("https://demo.minno.vn/dashboard/settings/customers/tags")
    page.get_by_placeholder("Tên thẻ").fill("Khách hàng Thân thiết")
    page.get_by_role("button", name="Thêm mới").click()
    expect(page.get_by_text("Đã thêm thẻ")).to_be_visible()

def test_add_customer_group(page: Page):
    """Test case: Thêm nhóm khách hàng mới"""
    page.goto("https://demo.minno.vn/dashboard/customers/groups")
    page.get_by_placeholder("Tên nhóm khách hàng").fill("Nhóm Khách VIP Python")
    page.get_by_role("button", name="Lưu").click()
    expect(page.get_by_text("Tạo nhóm thành công")).to_be_visible()
