"""
Test Suite 11: Universal Command Hub (Ctrl+K), Analytics & Feedback
===================================================================
Tests Spotlight command palette, Gamified XP tracking, active study timer,
and User Satisfaction feedback modal.
"""

import unittest
import time
from selenium.webdriver.common.by import By
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.command_hub_page import CommandHubPage
from selenium_tests.pages.research_tabs_page import AnalyticsModalPOM, FeedbackModalPOM

class TestCommandHubAndAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.hub = CommandHubPage(cls.driver, BASE_URL)
        cls.analytics = AnalyticsModalPOM(cls.driver, BASE_URL)
        cls.feedback = FeedbackModalPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_command_hub_open_and_close(self):
        """Verify opening Spotlight command palette and closing."""
        self.workspace.open_command_hub()
        time.sleep(0.5)
        self.assertTrue(self.hub.is_hub_open(), "Command hub palette should open")
        # Close by clicking ✕ or pressing ESC
        close_btn = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")
        if close_btn:
            close_btn[0].click()
            time.sleep(0.3)

    def test_02_analytics_and_rewards_modal(self):
        """Verify opening Research Analytics Hub displays XP points and rank progression."""
        self.workspace.safe_click(self.workspace.ANALYTICS_TRIGGER)
        time.sleep(0.5)
        self.assertTrue(self.analytics.is_visible(self.analytics.MODAL_CONTAINER, timeout=5), "Analytics modal should open")
        self.analytics.close()

    def test_03_satisfaction_feedback_modal(self):
        """Verify opening Feedback modal and submitting rating."""
        if self.workspace.is_visible(self.workspace.FEEDBACK_TRIGGER, timeout=3):
            self.workspace.safe_click(self.workspace.FEEDBACK_TRIGGER)
            time.sleep(0.5)
            self.feedback.submit_rating(stars=5, comment="Tested via Selenium Automation Framework - Pass!")
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
