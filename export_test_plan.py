import pandas as pd

# 1. Sheet: Kế hoạch kiểm thử (Test Plan)
test_plan = {
    'Hạng mục': ['Mục tiêu', 'Phạm vi', 'Môi trường', 'Công cụ', 'Loại kiểm thử', 'Tiêu chí Pass'],
    'Chi tiết': [
        'Đảm bảo luồng nghiệp vụ từ nhập hàng đến bán hàng và thanh toán hoạt động chính xác 100%.',
        'Module Sản phẩm, Đơn hàng, Kho vận, Tài chính, API và Database.',
        'Staging / UAT Environment (demo.minno.vn)',
        'Playwright (UI), Postman (API), SQL Server/MySQL (Database)',
        'E2E, Regression, UAT, Integration (API-DB)',
        '100% Test Case mức Critical và High phải Pass. Không có lỗi UI nghiêm trọng.'
    ]
}

# 2. Sheet: Kịch bản kiểm thử E2E (Test Scenarios)
test_scenarios = {
    'ID': ['TC01', 'TC02', 'TC03', 'TC04', 'TC05'],
    'Module': ['Sản phẩm', 'Sản phẩm', 'Đơn hàng', 'Thanh toán', 'Tài chính'],
    'Kịch bản': [
        'Tạo sản phẩm mới hoàn chỉnh và kiểm tra đồng bộ',
        'Cập nhật giá và tồn kho qua API',
        'Tạo đơn hàng POS và kiểm tra trừ kho thực tế',
        'Xác nhận thanh toán chuyển khoản và xuất hóa đơn',
        'Kiểm tra dòng tiền trong sổ quỹ sau khi hoàn tất đơn'
    ],
    'Các bước thực hiện': [
        '1. UI: Tạo SP -> 2. SQL: Check table products -> 3. API: GET /products/{id}',
        '1. Postman: PUT /products/update-stock -> 2. UI: Check số lượng hiển thị',
        '1. UI POS: Thêm SP, chọn khách -> 2. Thanh toán -> 3. SQL: Check table inventory_logs',
        '1. UI: Chọn thanh toán CK -> 2. API: Check payment_status == success',
        '1. SQL: SELECT * FROM transactions WHERE order_id = ... -> 2. UI: Check Sổ quỹ'
    ],
    'Kết quả mong đợi': [
        'Dữ liệu SP khớp giữa UI, API và SQL.',
        'Tồn kho cập nhật ngay lập tức, không sai lệch.',
        'Số lượng kho trừ đúng bằng số lượng bán. Log kho ghi nhận đúng.',
        'Trạng thái đơn thành Đã thanh toán. Mã hóa đơn trùng khớp.',
        'Số dư tài khoản tăng đúng bằng giá trị đơn hàng.'
    ],
    'Mức độ': ['Critical', 'High', 'Critical', 'Critical', 'High']
}

# 3. Sheet: SQL & API Verification
verification = {
    'Hệ thống': ['Database', 'Database', 'API', 'API'],
    'Bảng / Endpoint': ['products', 'inventory_stocks', '/api/v1/orders', '/api/v1/finance/transactions'],
    'Câu lệnh SQL / Method': [
        'SELECT name, sku, price FROM products WHERE sku = "{sku}"',
        'SELECT quantity FROM inventory_stocks WHERE product_id = {id}',
        'GET /orders?sku={sku} -> verify status, total_amount',
        'GET /transactions -> verify type, amount, reference_id'
    ],
    'Mục đích kiểm tra': [
        'Xác thực dữ liệu thô lưu xuống DB có bị lỗi font hay sai lệch giá không.',
        'Đảm bảo tính nhất quán của tồn kho khi có nhiều đơn hàng cùng lúc.',
        'Kiểm tra logic nghiệp vụ phía Backend cung cấp cho các kênh Shopee/Lazada.',
        'Đối soát dòng tiền thực tế với ghi nhận hệ thống.'
    ]
}

# Xuất ra Excel
file_path = 'MinnoSoft_E2E_TestPlan_Automation.xlsx'
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    pd.DataFrame(test_plan).to_excel(writer, sheet_name='Test Plan', index=False)
    pd.DataFrame(test_scenarios).to_excel(writer, sheet_name='Test Scenarios E2E', index=False)
    pd.DataFrame(verification).to_excel(writer, sheet_name='SQL & API Checks', index=False)

print(f'File Excel đã được tạo tại: {file_path}')
