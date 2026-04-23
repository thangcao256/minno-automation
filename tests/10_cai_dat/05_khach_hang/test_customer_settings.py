import allure
from pages.settings.customer_page import SettingsCustomerPage
from playwright.sync_api import Page

@allure.epic("Settings")
@allure.feature("Customer Config")
@allure.severity(allure.severity_level.CRITICAL)
class TestCustomerSettings:

    @allure.story("Create Customer Tag")
    def test_create_customer_tag(self, page: Page, run_id):
        cust_settings = SettingsCustomerPage(page)
        cust_settings.navigate_to_tab("tag")
        # Sử dụng hàm 'and_exit' để đóng Drawer sau khi tạo
        cust_settings.create_config_and_exit(f"Tag_{run_id}")

    @allure.story("Create Customer Group")
    def test_create_customer_group(self, page: Page, run_id):
        cust_settings = SettingsCustomerPage(page)
        cust_settings.navigate_to_tab("customer_group")
        cust_settings.create_config_and_exit(f"Group_{run_id}")

    @allure.story("Create Customer Rank")
    def test_create_customer_rank(self, page: Page, run_id, test_data):
        rank_data = test_data['customer_ranks'][0]
        unique_rank_name = f"{rank_data['name']} {run_id}"
        
        cust_settings = SettingsCustomerPage(page)
        cust_settings.navigate_to_tab("rank")
        # Hạng khách hàng cũng dùng chung Drawer, ta gọi and_exit luôn
        cust_settings.create_config_and_exit(unique_rank_name)
