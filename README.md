# 🚀 MinnoSoft E2E Automation Testing Framework

[![CI/CD E2E Regression](https://github.com/thangcao256/minno-automation/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/thangcao256/minno-automation/actions/workflows/ci-cd.yml)
[![View Allure Report](https://img.shields.io/badge/Allure_Report-Online-brightgreen?style=flat-square&logo=github)](https://thangcao256.github.io/minno-automation/)

Bộ khung kiểm thử tự động toàn diện cho hệ thống quản lý bán hàng đa kênh **MinnoSoft (minno.vn)**.

## 📊 Báo cáo kiểm thử trực tuyến
Kết quả chạy test, ảnh chụp màn hình và video lỗi được cập nhật tự động tại:
👉 **[Xem Allure Report trực tuyến](https://thangcao256.github.io/minno-automation/)**

## ⚙️ CI/CD & Quản lý bộ test (Test Suite)
Dự án được tích hợp tự động hóa qua GitHub Actions. Bạn có thể kiểm soát các test case sẽ chạy trên server:

1.  **Quản lý bộ test:** Mở file `test_suite.txt`.
    *   Thêm đường dẫn file test mới để kích hoạt chạy trên CI.
    *   Thêm dấu `#` vào đầu dòng để tạm thời bỏ qua test case đó.
2.  **Xem Log chi tiết:**
    *   Vào tab **Actions** trên GitHub.
    *   Chọn lần chạy (Workflow Run) gần nhất.
    *   Nhấn vào Job **Run E2E Tests** để xem log chi tiết từng bước.
3.  **Tải Artifacts:** Ảnh chụp màn hình lỗi và video được lưu trong mục **Artifacts** ở cuối mỗi lần chạy.

---

## 📌 Tổng quan dự án
Dự án này tập trung vào việc tự động hóa các luồng nghiệp vụ quan trọng (Master Business Flow):
* **Quản trị:** Phân quyền nhân viên, cấu hình chi nhánh.
* **Sản phẩm:** Danh mục, thuộc tính biến thể, nhà cung cấp.
* **Kênh bán hàng:** Quản lý khách hàng, nhóm VIP, tích điểm.
* **Marketing:** Chương trình khuyến mãi, Voucher.

## 🏗️ Kiến trúc Framework
* **Ngôn ngữ:** Python 3.10+
* **Công cụ lõi:** [Playwright](https://playwright.dev/python/)
* **Test Runner:** [Pytest](https://docs.pytest.org/)
* **Báo cáo:** Allure Report & GitHub Pages.
* **Tích hợp:** GitHub Actions (Trigger on Push/Schedule).

## 📁 Cấu trúc thư mục (3-Tier Menu)
```text
minno-automation/
├── tests/                  # Kịch bản kiểm thử (Test Cases)
├── pages/                  # Page Object Model (POM)
├── test_data/              # Dữ liệu & Ảnh mẫu
├── test_suite.txt          # Danh sách test case chạy trên CI/CD
├── conftest.py             # Fixtures (Đăng nhập tự động)
└── .github/workflows/      # Cấu hình GitHub Actions
```

## ⚙️ Cài đặt & Sử dụng

### 1. Chuẩn bị môi trường (Windows)
```bash
./setup.bat
```

### 2. Cấu hình tài khoản
Tạo file `.env` và điền thông tin (trên GitHub hãy điền vào mục **Secrets**):
```env
BASE_URL=https://demo.minno.vn
ADMIN_USER=your_email@minno.vn
ADMIN_PASS=your_password
```

### 3. Chạy kiểm thử local
* **Chạy theo bộ suite:** `pytest $(grep -v '^#' test_suite.txt)`
* **Chạy có giao diện:** `pytest --headed`

---
*Phát triển bởi Đội ngũ QA Automation - 2026*
