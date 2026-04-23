from playwright.sync_api import Page, expect
import os
import re

def test_add_product_category_robust(page: Page, test_data, run_id):
    """[TEST CASE] - Thêm Danh mục sản phẩm (tab=category)"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    category = test_data['catalog_test']['categories'][0]
    unique_name = f"{category['name']} {run_id}"
    unique_code = f"{category['code']}_{run_id.replace('_', '')}"
    
    page.goto(f"{base_url}/product/category?tab=category")
    
    # Click Thêm (Selector đã okie)
    page.locator('//*[@id="root"]/div/div/main/div/div/div[1]/div/div[2]/button').first.click()
    
    # Nhập thông tin
    page.locator('input[name="name"]').fill(unique_name)
    code_input = page.locator('input[name="code"]')
    if code_input.is_visible():
        code_input.fill(unique_code)
    
    # Lưu
    page.locator("div[role='dialog'] button").filter(has_text=re.compile(r"Lưu|Xác nhận|Save|Confirm", re.I)).first.click()
    
    # 6. Xác nhận (Scroll -> Click -> Verify Text)
    # Đợi item xuất hiện trong danh sách, cuộn tới và click
    new_supplier_link = page.get_by_text(unique_name).first
    new_supplier_link.scroll_into_view_if_needed()
    new_supplier_link.click()

    # Kiểm tra Header trang chi tiết (Thường nằm trong thẻ h1 hoặc h2)
    # Sử dụng expect với to_have_text để có cơ chế retry tự động
    expect(page.locator("h1, h2").filter(has_text=unique_name).first).to_be_visible(timeout=10000)

def test_add_product_group_robust(page: Page, test_data, run_id):
    """[TEST CASE] - Thêm Nhóm sản phẩm (tab=group)"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    group = test_data['catalog_test']['groups'][0]
    unique_name = f"{group['name']} {run_id}"
    unique_code = f"{group['code']}_{run_id.replace('_', '')}"
    
    page.goto(f"{base_url}/product/category?tab=group")
    
    # Click Thêm (Selector đã okie)
    page.locator('//*[@id="root"]/div/div/main/div/div/div[1]/div/div[2]/button').first.click()
    
    page.locator('input[name="name"]').fill(unique_name)
    page.locator('input[name="code"]').fill(unique_code)
    
    # Lưu
    page.locator("div[role='dialog'] button").filter(has_text=re.compile(r"Lưu|Xác nhận|Save|Confirm", re.I)).first.click()
    
    expect(page.get_by_text(unique_name).first).to_be_visible(timeout=10000)

def test_add_product_supplier_robust(page: Page, test_data, run_id):
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    supplier = test_data['catalog_test']['suppliers'][1]

    unique_name = f"{supplier['name']} {run_id}"
    unique_code = f"{supplier['code']}_{run_id.replace('_', '')}"

    page.goto(f"{base_url}/product/category?tab=supplier")

    # 1. Mở modal (ưu tiên role/text)
    page.locator('//*[@id="root"]/div/div/main/div/div/div[1]/div/div[2]/button').first.click()

    # 2. Input cơ bản
    page.locator('input[name="name"]').fill(unique_name)
    page.locator('input[name="code"]').fill(unique_code)

    if page.locator('input[name="email"]').is_visible():
        page.locator('input[name="email"]').fill(supplier['email'])

    if page.locator('input[name="phone_number"]').is_visible():
        page.locator('input[name="phone_number"]').fill(supplier['phone'])

    # 🔥 3. Hàm reusable chọn dropdown (Cực kỳ linh hoạt cho Tỉnh/Quận/Xã)
    def select_dropdown(label_pattern, value):
        try:
            # Bước 1: Tìm và click vào ô chọn (Trigger)
            # Ưu tiên tìm trong container space-y-1 có chứa label tương ứng
            trigger = page.locator("div.space-y-1").filter(has_text=re.compile(label_pattern, re.I)).locator("[role='combobox'], button").first

            if not trigger.is_visible(timeout=2000):
                # Dự phòng: Tìm bất kỳ button/combo nào chứa text label
                trigger = page.locator("[role='combobox'], button").filter(has_text=re.compile(label_pattern, re.I)).first

            trigger.click()
            page.wait_for_timeout(500) # Đợi danh sách bung ra

            # Bước 2: Tìm Option trong danh sách
            # Linh hoạt: value="26" có thể khớp với "Phường 26" hoặc "26"
            # Ta dùng Regex không bắt đầu/kết thúc chặt chẽ để chấp nhận prefix
            option = page.locator("[role='option'], .select-item, [data-radix-collection-item] div").filter(has_text=re.compile(str(value), re.I)).first

            if option.is_visible(timeout=3000):
                option.scroll_into_view_if_needed()
                option.click()
                return

            # Bước 3: Dự phòng cuối cùng - Quét toàn trang và click vào text đúng nhất
            # Ưu tiên lấy cái cuối cùng (.last) vì thường dropdown list nằm ở cuối DOM
            direct_target = page.get_by_text(re.compile(str(value), re.I)).last
            direct_target.scroll_into_view_if_needed()
            direct_target.click()

        except Exception as e:
            print(f"Cảnh báo: Không thể chọn '{value}' cho '{label_pattern}'. Lỗi: {e}")

    # 4. Thực hiện chọn lần lượt 3 cấp địa chỉ
    select_dropdown("tỉnh|thành", supplier['city'])
    page.wait_for_timeout(1000) # Đợi API load dữ liệu Quận

    select_dropdown("quận|huyện", supplier['district'])
    page.wait_for_timeout(1000) # Đợi API load dữ liệu Xã

    select_dropdown("phường|xã", supplier['ward'])


    # 5. Địa chỉ chi tiết
    if page.locator('input[name="detail_address"]').is_visible():
        page.locator('input[name="detail_address"]').fill(supplier['address'])

    # 6. Save
    page.locator('//*[@id="radix-_r_0_"]/div[3]/button[2]').first.click()

    # 7. Verify (Scroll -> Click -> Check Header)
    # Tìm liên kết/dòng chứa tên nhà cung cấp vừa tạo
    # new_item = page.get_by_text(unique_name).first
    # new_item.scroll_into_view_if_needed()
    # new_item.click()

    # Xác nhận tiêu đề trang chi tiết
    # expect(page.locator("h1, h2, .header-title").filter(has_text=unique_name).first).to_be_visible(timeout=10000)
def test_add_product_attribute_robust(page: Page, test_data, run_id):
    """[TEST CASE] - Thêm Thuộc tính (tab=attribute) - Name & Values list"""
    base_url = os.getenv("BASE_URL", "https://demo.minno.vn")
    attribute = test_data['catalog_test']['attributes'][0] # Kích thước (values: S, M, L, XL)
    unique_name = f"{attribute['name']} {run_id}"

    page.goto(f"{base_url}/product/category?tab=attribute")

    # 1. Mở Modal - Sử dụng XPath theo yêu cầu
    page.locator('//*[@id="root"]/div/div/main/div/div/div[1]/div/div[2]/button').first.click()

    # 2. Nhập Tên thuộc tính
    page.locator('input[name="name"]').fill(unique_name)

    # 3. Nhập các Giá trị thuộc tính (Values)
    # Vòng lặp nhập từng giá trị: Nhập -> Bấm Thêm (trừ giá trị cuối cùng)
    values_list = attribute['values']
    if values_list:
        for i, val in enumerate(values_list):
            # Luôn chọn ô input cuối cùng để điền
            current_input = page.locator("div[role='dialog'] input:not([name='name']):not([type='checkbox']):not([type='radio'])").last
            current_input.fill(val)
            
            # Nếu chưa phải giá trị cuối cùng thì mới bấm nút Thêm để hiện ô mới
            if i < len(values_list) - 1:
                # Bấm nút Thêm giá trị - Sử dụng XPath theo yêu cầu
                page.locator('//*[@id="radix-_r_0_"]/div[2]/div/div/div/form/div/div[3]/label/span').first.click()
                # Đợi UI tạo ô input mới
                page.wait_for_timeout(800)

    # 4. Lưu - Sử dụng XPath gốc
    page.locator('//*[@id="radix-_r_0_"]/div[3]/button[2]').first.click()

    # 5. Xác nhận
    expect(page.get_by_text(unique_name).first).to_be_visible(timeout=10000)

