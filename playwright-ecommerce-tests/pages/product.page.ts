import { Page, Locator } from '@playwright/test';
import { BasePage } from './base.page';

export class ProductPage extends BasePage {
  readonly productName: Locator;
  readonly basePrice: Locator;
  readonly saveButton: Locator;

  constructor(page: Page) {
    super(page);
    this.productName = page.getByPlaceholder('Nhập tên sản phẩm');
    this.basePrice = page.locator('input[name="basePrice"]');
    this.saveButton = page.getByTestId('button-save-product');
  }

  async createProduct(name: string, price: string) {
    await this.productName.fill(name);
    await this.basePrice.fill(price);
    await this.saveButton.click();
  }
}
