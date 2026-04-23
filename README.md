# 🚀 MinnoSoft E2E Automation Testing Framework

Bộ khung kiểm thử tự động toàn diện cho hệ thống quản lý bán hàng đa kênh **MinnoSoft (minno.vn)**. Framework được thiết kế theo mô hình chuyên nghiệp, tối ưu cho việc duy trì lâu dài và tích hợp vào quy trình CI/CD.

## 📌 Tổng quan dự án
Dự án này tập trung vào việc tự động hóa các luồng nghiệp vụ quan trọng (Master Business Flow) của MinnoSoft, bao gồm:
* **Quản trị:** Phân quyền nhân viên, cấu hình chi nhánh, quản lý vai trò.
* **Sản phẩm:** Danh mục, nhóm hàng, thuộc tính biến thể, nhà cung cấp.
* **Kênh bán hàng:** Quản lý khách hàng, nhóm VIP, tích điểm.
* **Marketing:** Chương trình khuyến mãi, Voucher, chiến dịch quảng cáo.

## 🏗️ Kiến trúc Framework
* **Ngôn ngữ:** Python 3.13+
* **Công cụ lõi:** [Playwright](https://playwright.dev/python/) (Tốc độ cao, tự động đợi phần tử).
* **Test Runner:** [Pytest](https://docs.pytest.org/) (Fixture-based, linh hoạt).
* **Mô hình thiết kế:** Page Object Model (POM) & Data-driven Testing.
* **Báo cáo:** Allure Report & Pytest-HTML.
* **Tích hợp:** GitHub Actions (Chạy định kỳ 00:00 Thứ Hai hàng tuần).

## 📁 Cấu trúc thư mục (3-Tier Menu)
Bộ test được tổ chức khớp 1:1 với Menu Sidebar của MinnoSoft:
```text
minno-automation/
├── tests/                  # Kịch bản kiểm thử (Test Cases)
│   ├── 01_trang_chu/       # Đăng nhập, Dashboard
│   ├── 03_san_pham/        # Danh mục, Nguồn hàng, Thuộc tính
│   ├── 05_kenh_ban_hang/   # Khách hàng, Nhóm khách
│   ├── 10_cai_dat/         # Phân quyền, Cửa hàng
│   └── 11_dang_xuat/       # Logout an toàn
├── pages/                  # Page Object Model (Đang refactor)
├── test_data.json          # Dữ liệu kiểm thử tập trung (JSON)
├── UI/                     # Snapshots HTML hỗ trợ phân tích Offline
├── conftest.py             # Fixtures (Đăng nhập tự động, Setup môi trường)
├── export_test_plan.py     # Tool xuất Test Plan ra file Excel chuyên nghiệp
├── setup.bat               # File cài đặt môi trường tự động (Windows)
└── .env                    # Biến môi trường (URL, Tài khoản - Bảo mật)
```

## ⚙️ Cài đặt & Sử dụng

### 1. Chuẩn bị môi trường
Trên Windows, bạn chỉ cần chạy file script để tự động hóa mọi bước:
```bash
./setup.bat
```
*Script sẽ tự động: Tạo venv, cài thư viện, cài browser Chromium.*

### 2. Cấu hình tài khoản
Tạo file `.env` từ `.env.example` và điền thông tin:
```env
BASE_URL=https://demo.minno.vn
ADMIN_USER=your_email@minno.vn
ADMIN_PASS=your_password
STORE=TC  # Chi nhánh mặc định
```

### 3. Chạy kiểm thử
* **Chạy tất cả (Headless):**
  ```bash
  pytest
  ```
* **Chạy có giao diện (Debug):**
  ```bash
  pytest --headed
  ```
* **Chạy module cụ thể:**
  ```bash
  pytest tests/03_san_pham/
  ```

## 📊 Báo cáo & Kế hoạch
* **Báo cáo HTML:** Tự động tạo sau khi chạy trong thư mục `report.html`.
* **Kế hoạch kiểm thử (Excel):** Chạy `python export_test_plan.py` để nhận file `MinnoSoft_E2E_TestPlan_Automation.xlsx` bao gồm các kịch bản SQL & API.

## 🔐 Bảo mật (Security)
* File `.env` chứa thông tin nhạy cảm đã được cấu hình trong `.gitignore` để không đẩy lên GitHub.
* Trên CI/CD (GitHub Actions), các thông tin này được quản lý qua **Repository Secrets**.

## 🧠 Best Practices áp dụng
* **Immutable Selectors:** Ưu tiên dùng `role`, `alt`, `type` thay vì các class CSS dễ thay đổi.
* **No Hardcoded Data:** 100% dữ liệu test (SKU, Tên sản phẩm, Vai trò) lấy từ `test_data.json` kèm hậu tố `run_id` (Time-based) để tránh trùng lặp.
* **Auto-Login:** Hệ thống tự động xử lý login và chọn cửa hàng tại `conftest.py`, giúp từng test case chỉ tập trung vào nghiệp vụ chính.

---
*Phát triển bởi Đội ngũ QA Automation - 2026*
