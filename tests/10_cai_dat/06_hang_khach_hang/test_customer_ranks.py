import allure
from pages.settings.rank_page import SettingsRankPage
from playwright.sync_api import Page

@allure.epic("Settings")
@allure.feature("Customer Ranks")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_customer_rank_robust(page: Page, run_id, test_data):
    """
    [TC-RANK-01]: Verify creating a new Customer Rank in a dedicated module.
    """
    rank_data = test_data['customer_ranks'][0]
    unique_name = f"{rank_data['name']} {run_id}"
    
    rank_page = SettingsRankPage(page)
    rank_page.navigate_to_ranks()
    rank_page.create_rank(
        name=unique_name,
        min_spend=str(rank_data['min_spend']),
        discount=str(rank_data['discount'])
    )
