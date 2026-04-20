from playwright.sync_api import Page, expect

def test_create_role(page: Page, test_data):
    """Test case: Tạo nhóm quyền (Vai trò) mới"""
    role = test_data['roles'][1] # Sales
    page.goto("https://demo.minno.vn/dashboard/settings/roles/new")
    
    # Placeholder thực tế từ UI snapshot: "Nhập tên vai trò"
    page.get_by_placeholder("Nhập tên vai trò").fill(role['name'])
    
    # Nhấn nút Lưu
    page.get_by_role("button", name="Lưu").click()
    
    # Xác nhận thành công (Sử dụng Toast message hoặc text hiển thị)
    expect(page.get_by_text("Tạo vai trò thành công")).to_be_visible()

def test_add_staff(page: Page):
    """Test case: Thêm nhân viên mới vào hệ thống"""
    page.goto("https://demo.minno.vn/dashboard/settings/users/new")
    
    # Nhập thông tin nhân viên dựa trên UI thực tế
    page.get_by_placeholder("Họ và tên").fill("Nguyễn Văn Sales")
    page.get_by_placeholder("Số điện thoại").fill("0987654321")
    page.get_by_placeholder("Email").fill("sales@minno.vn")
    
    # Chọn vai trò (Dùng combo box)
    page.get_by_role("combobox", name="Vai trò").click()
    page.get_by_text("Sales").click()
    
    # Nhấn Lưu
    page.get_by_role("button", name="Lưu").click()
    expect(page.get_by_text("Thêm nhân viên thành công")).to_be_visible()
