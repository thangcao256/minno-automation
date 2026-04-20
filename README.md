# 🚀 MinnoSoft E2E Automation Testing Framework

Bộ khung kiểm thử tự động toàn diện cho hệ thống quản lý bán hàng đa kênh **MinnoSoft (minno.vn)**. Được xây dựng nhằm mục tiêu kiểm thử luồng nghiệp vụ chính (Master Business Flow) một cách ổn định, bảo mật và dễ bảo trì.

## 🛠 Công nghệ sử dụng (Tech Stack)

*   **Ngôn ngữ:** Python 3.13+
*   **Thư viện kiểm thử:** [Pytest](https://docs.pytest.org/)
*   **Công cụ Automation:** [Playwright](https://playwright.dev/python/)
*   **Báo cáo:** Pytest-HTML
*   **CI/CD:** GitHub Actions

## 📂 Cấu trúc thư mục (3-Tier Menu)

Bộ test được tổ chức theo cấu trúc 3 lớp, khớp hoàn toàn với Menu Sidebar của MinnoSoft:
```text
tests/
├── 01_trang_chu/           # Đăng nhập và Kiểm tra Dashboard
├── 02_don_hang/            # Quản lý đơn hàng
├── 03_san_pham/            # Danh sách sản phẩm, Danh mục
├── ...                     # Các module khác (04 -> 10)
└── 11_dang_xuat/           # Quy trình đăng xuất an toàn
```

## ⚙️ Cài đặt môi trường (Setup)

### 1. Dành cho người dùng Windows (Nhanh nhất)
1.  Clone dự án về máy.
2.  Nhấp đúp chuột vào file `setup.bat`. 
    *   *Nó sẽ tự động tạo môi trường ảo (.venv), cài thư viện và tải trình duyệt Chromium.*
3.  Tạo file `.env` bằng cách copy từ `.env.example` và điền tài khoản test của bạn.

### 2. Cấu hình PyCharm
1.  Mở dự án trong PyCharm.
2.  Vào `Settings` -> `Project` -> `Python Interpreter`.
3.  Chọn **Add Interpreter** -> **Existing** -> Trỏ đến đường dẫn: `.venv\Scripts\python.exe`.
4.  Lúc này, các nút **mũi tên xanh** sẽ xuất hiện cạnh từng test case để bạn nhấn chạy lẻ.

## 🏃 Cách chạy kiểm thử

### Chạy thủ công (Manual)
*   **Chạy lẻ:** Nhấn nút mũi tên xanh trực tiếp trong PyCharm.
*   **Chạy toàn bộ:** Mở Terminal và gõ:
    ```bash
    pytest
    ```

### Chạy tự động (Automation)
*   Hệ thống tự động chạy vào **00:00 sáng Thứ Hai** hàng tuần trên GitHub Actions.
*   Báo cáo HTML kèm hình ảnh/video lỗi sẽ được đính kèm trong phần **Artifacts**.

## 🔐 Bảo mật (Security)
*   Thông tin tài khoản (`ADMIN_USER`, `ADMIN_PASS`) được lưu tại file `.env`.
*   File `.env` đã được cấu hình trong `.gitignore` để **không bao giờ bị đẩy lên Git**, đảm bảo an toàn tuyệt đối cho tài khoản doanh nghiệp.

## 📊 Chiến lược Selector
Framework sử dụng chiến thuật **Selector Bất biến (Immutable)**:
*   Ưu tiên: `type="password"`, `type="submit"`, `alt="Logo"`.
*   Không phụ thuộc vào ngôn ngữ hiển thị (Tiếng Anh/Tiếng Việt đều chạy đúng).
*   Tự động xử lý luồng đăng nhập 2 bước và chọn chi nhánh theo biến môi trường `STORE`.

---
*Phát triển bởi Đội ngũ QA Automation - 2026*
