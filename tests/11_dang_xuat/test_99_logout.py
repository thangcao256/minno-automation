import allure
from pages.dashboard.dashboard_page import DashboardPage
from playwright.sync_api import Page

@allure.epic("Authentication")
@allure.feature("Logout")
@allure.severity(allure.severity_level.BLOCKER)
def test_99_logout_robust(page: Page):
    """
    [TC-LOGOUT-01]: Verify user can logout successfully and session is cleared.
    """
    dashboard = DashboardPage(page)
    
    # Ensure we are on Dashboard first
    dashboard.verify_dashboard_ready()
    
    # Execute Logout
    dashboard.logout()
    
    # Final check: URL should contain auth or login
    assert "auth" in page.url or "login" in page.url
