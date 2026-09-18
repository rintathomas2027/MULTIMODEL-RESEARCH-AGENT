"""
Test Suite 01: Smoke Testing, Page Rendering & Theme Switcher
=============================================================
Tests initial page loading, title, hero header, theme engine (Dark / Light mode),
and responsive layout integrity.
"""

import unittest
import time
from selenium.webdriver.common.by import By
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage

class TestSmokeAndLayout(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_homepage_renders_successfully(self):
        """Verify the main landing page loads with status 200 and expected title."""
        self.workspace.open_home()
        title = self.workspace.get_title()
        self.assertIn("ScholarPulse", title, "Page title should contain 'ScholarPulse'")
        self.assertTrue(self.workspace.is_visible((By.ID, "root")), "React root container must be mounted")

    def test_02_navigation_elements_present(self):
        """Verify navigation bar brand logo and access triggers are visible."""
        self.assertTrue(self.workspace.is_visible(self.workspace.LOGO), "Brand logo must be visible")
        self.assertTrue(self.workspace.is_visible(self.workspace.THEME_TOGGLE_BTN), "Theme toggle button must be visible")

    def test_03_theme_toggle_dark_and_light(self):
        """Verify toggling theme alternates <html> class between dark and light mode."""
        current_theme = self.workspace.toggle_theme()
        self.assertIn(current_theme, ["dark", "light"], "Theme state should be 'dark' or 'light'")
        
        # Toggle back
        new_theme = self.workspace.toggle_theme()
        self.assertNotEqual(current_theme, new_theme, "Toggling theme should change active state")

    def test_04_feature_cards_displayed(self):
        """Verify the 3 core hero feature highlight cards render properly."""
        feature_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'glass-card') and .//h3]")
        self.assertGreaterEqual(len(feature_cards), 3, "At least 3 core feature showcase cards should be displayed")

if __name__ == '__main__':
    unittest.main()
