"""
Test Suite 02: Authentication, Validation, Guest Access & Profile
=================================================================
Tests User Registration, Login, Client-side Form Validation,
Instant 1-Click Guest Mode, and Logout workflows.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL, TEST_USER
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.auth_modal_page import AuthModalPage

class TestAuthAndUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.auth = AuthModalPage(cls.driver, BASE_URL)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def setUp(self):
        self.workspace.open_home()

    def test_01_open_and_close_auth_modal(self):
        """Verify opening and closing the Authentication modal."""
        self.workspace.open_auth_modal()
        self.assertTrue(self.auth.is_modal_open(), "Auth modal should be open")
        self.auth.close_modal()
        time.sleep(0.3)
        self.assertFalse(self.auth.is_modal_open(), "Auth modal should close when clicking ✕")

    def test_02_instant_guest_researcher_access(self):
        """Verify 1-Click Guest Access logs the user in without credentials."""
        self.workspace.open_auth_modal()
        self.auth.click_guest_access()
        time.sleep(1)
        # Should now be inside workspace
        self.assertTrue(self.workspace.is_visible(self.workspace.LOGOUT_BTN, timeout=5), "User should be logged in as guest")

    def test_03_form_validation_short_username(self):
        """Verify client-side validation for short username."""
        self.workspace.logout()
        self.workspace.open_auth_modal()
        self.auth.register("ab", "valid@email.com", "validpassword123")
        err = self.auth.get_error_message()
        self.assertIn("at least 3 characters", err, "Should show validation error for short username")
        self.auth.close_modal()

    def test_04_form_validation_invalid_email(self):
        """Verify client-side validation for malformed email."""
        self.workspace.open_auth_modal()
        self.auth.register("validuser", "invalid-email", "validpassword123")
        err = self.auth.get_error_message()
        self.assertIn("valid email", err.lower(), "Should show validation error for invalid email")
        self.auth.close_modal()

    def test_05_register_new_scholar_account(self):
        """Verify successful user registration with valid credentials."""
        unique_user = f"scholar_{int(time.time())}"
        self.workspace.open_auth_modal()
        self.auth.register(unique_user, f"{unique_user}@university.edu", "ValidPass@2026")
        time.sleep(1.5)
        self.assertTrue(self.workspace.is_visible(self.workspace.LOGOUT_BTN, timeout=5), "User should be logged in after registration")
        self.workspace.logout()

if __name__ == '__main__':
    unittest.main()
