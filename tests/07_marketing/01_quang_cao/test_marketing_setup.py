import allure
from pages.marketing.marketing_page import MarketingPage
from playwright.sync_api import Page

@allure.epic("Marketing")
@allure.feature("Promotions")
@allure.severity(allure.severity_level.NORMAL)
def test_create_promotion_robust(page: Page, run_id):
    """
    [TC-MARK-01]: Verify creating a new marketing promotion.
    """
    marketing = MarketingPage(page)
    marketing.navigate_to_new_promotion()
    marketing.create_promotion(f"Campaign Summer {run_id}")

@allure.epic("Marketing")
@allure.feature("Vouchers")
@allure.severity(allure.severity_level.NORMAL)
def test_create_voucher_robust(page: Page, run_id):
    """
    [TC-MARK-02]: Verify creating a new discount voucher.
    """
    marketing = MarketingPage(page)
    marketing.navigate_to_new_voucher()
    marketing.create_voucher(f"VOUCHER_{run_id}", "20")
