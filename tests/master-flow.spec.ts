import { test, expect } from '@playwright/test';
import * as testData from '../test_data.json';

test.describe('Minno E2E: Master Business Flow', () => {
  
  test.beforeEach(async ({ page }) => {
    // Giả sử đã đăng nhập qua storageState hoặc thực hiện login tại đây
    await page.goto('/dashboard');
  });

  test('Step 1-2: Setup Roles and Staff', async ({ page }) => {
    const role = testData.roles[1]; // Sales
    await page.goto('/dashboard/settings/roles/new');
    await page.getByPlaceholder('Nhập tên vai trò').fill(role.name);
    // Logic check các checkbox quyền dựa trên role.permissions...
    await page.getByRole('button', { name: 'Lưu' }).click();
    await expect(page.getByText('Tạo vai trò thành công')).toBeVisible();
  });

  test('Step 3-4: Customer and Product Categories', async ({ page }) => {
    // Thêm Danh mục sản phẩm
    await page.goto('/dashboard/products/categories');
    await page.getByRole('button', { name: 'Thêm danh mục' }).click();
    await page.locator('input[name="categoryName"]').fill('Điện tử gia dụng');
    await page.getByRole('button', { name: 'Xác nhận' }).click();
    
    // Thêm Nhóm khách hàng
    await page.goto('/dashboard/customers/groups');
    await page.getByPlaceholder('Tên nhóm khách hàng').fill('Khách hàng VIP');
    await page.getByRole('button', { name: 'Lưu' }).click();
  });

  test('Step 5: Create Product with Variations', async ({ page }) => {
    const product = testData.products[0]; // iPhone 15
    await page.goto('/dashboard/products/create');
    await page.getByPlaceholder('Nhập tên sản phẩm').fill(product.name);
    await page.locator('input[name="sku"]').fill(product.sku);
    await page.locator('input[name="basePrice"]').fill(product.price.toString());
    
    // Thêm thuộc tính (Color, Storage)
    await page.getByText('Thêm thuộc tính').click();
    // Logic chọn thuộc tính và nhập giá trị...
    
    await page.getByRole('button', { name: 'Lưu sản phẩm' }).click();
    await expect(page).toHaveURL(/\/dashboard\/products$/);
  });

  test('Step 6-7: Promotion and Order Creation', async ({ page }) => {
    // Tạo mã giảm giá
    await page.goto('/dashboard/promotions/vouchers/new');
    await page.getByPlaceholder('Mã voucher').fill('MINNO2026');
    await page.locator('input[name="discountValue"]').fill('10'); // 10%
    await page.getByRole('button', { name: 'Phát hành' }).click();

    // Tạo đơn hàng
    await page.goto('/dashboard/orders/new');
    await page.getByPlaceholder('Tìm khách hàng').fill(testData.customers[0].name);
    await page.keyboard.press('Enter');
    
    await page.getByPlaceholder('Tìm sản phẩm').fill(testData.products[0].name);
    await page.keyboard.press('Enter');

    // Áp dụng mã giảm giá
    await page.getByPlaceholder('Mã giảm giá').fill('MINNO2026');
    await page.getByRole('button', { name: 'Áp dụng' }).click();

    await page.getByRole('button', { name: 'Tạo đơn hàng' }).click();
    await expect(page.getByText('Đơn hàng đã được tạo')).toBeVisible();
  });
});
