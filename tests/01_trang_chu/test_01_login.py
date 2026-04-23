from pages.dashboard.dashboard_page import DashboardPage
from playwright.sync_api import Page

def test_01_login_to_minnosoft(page: Page):
    """
    [TC-LOGIN-01]: Verify successful login and Dashboard readiness.
    Uses Page Object Model (POM) to validate the system state after login.
    """
    dashboard = DashboardPage(page)
    dashboard.verify_dashboard_ready()
