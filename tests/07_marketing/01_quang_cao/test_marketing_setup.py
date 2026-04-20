from playwright.sync_api import Page, expect

def test_add_promotion(page: Page):
    """Test case: Thêm chương trình khuyến mãi mới"""
    page.goto("https://demo.minno.vn/dashboard/promotions/new")
    
    # Nhập thông tin chương trình
    page.get_by_placeholder("Tên chương trình").fill("Chiến dịch Python Mùa Hè 2026")
    
    # Nhấn Lưu
    page.get_by_role("button", name="Lưu").click()
    expect(page.get_by_text("Tạo khuyến mãi thành công")).to_be_visible()

def test_add_voucher(page: Page):
    """Test case: Thêm mã giảm giá (Voucher) mới"""
    page.goto("https://demo.minno.vn/dashboard/promotions/vouchers/new")
    
    # Nhập mã voucher
    page.get_by_placeholder("Mã voucher").fill("MINNO_PY_15")
    page.locator('input[name="discountValue"]').fill("15")
    
    # Nhấn Phát hành/Xác nhận
    page.get_by_role("button", name="Xác nhận").click()
    expect(page.get_by_text("Phát hành thành công")).to_be_visible()
