import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/login.page';
import * as users from '../../test-data/users.json';

test.describe('Authentication Tests', () => {
  test('Should login successfully with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.navigateTo('/login');
    await loginPage.login(users[0].username, users[0].password);
    
    // Validate redirect or success message
    await expect(page).toHaveURL(/\/dashboard/);
  });
});
