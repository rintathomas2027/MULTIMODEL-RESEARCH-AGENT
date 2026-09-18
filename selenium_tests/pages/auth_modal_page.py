"""
ScholarPulse AI Studio - Authentication & Profile Modal Page Object
===================================================================
Handles User Registration, Login, Form Validations, Guest Mode,
and User Profile customizations.
"""

import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class AuthModalPage(BasePage):
    """Page Object for Authentication and Profile Modals."""

    # Auth Modal Locators
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//form]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")
    GUEST_ACCESS_BTN = (By.XPATH, "//button[contains(., 'Instant Guest Researcher Access')]")
    TOGGLE_MODE_BTN = (By.XPATH, "//button[contains(text(), 'Already have an account?') or contains(text(), 'Need an account?')]")
    
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='e.g. scholar_researcher' or @type='text']")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or @placeholder='e.g. scholar@university.edu']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @placeholder='••••••••']")
    SUBMIT_BTN = (By.XPATH, "//form//button[@type='submit']")
    ERROR_BOX = (By.XPATH, "//div[contains(@class, 'bg-rose-500')]")

    # Profile Modal Locators
    PROFILE_MODAL = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//h3[contains(text(), 'Profile') or contains(text(), 'Settings')]]")
    RESEARCH_INTERESTS_INPUT = (By.XPATH, "//textarea[@placeholder='e.g. Deep Learning, Multi-Agent Systems' or contains(@class, 'rounded-xl')]")
    SAVE_PROFILE_BTN = (By.XPATH, "//button[contains(text(), 'Save Profile Changes')]")

    def is_modal_open(self):
        return self.is_visible(self.MODAL_CONTAINER, timeout=3)

    def close_modal(self):
        if self.is_visible(self.CLOSE_BTN, timeout=2):
            self.safe_click(self.CLOSE_BTN)
            time.sleep(0.3)
        return self

    def click_guest_access(self):
        self.safe_click(self.GUEST_ACCESS_BTN)
        time.sleep(0.5)
        return self

    def switch_to_login_mode(self):
        btn = self.wait_for_visible(self.TOGGLE_MODE_BTN)
        if "Already have an account" in btn.text or "Sign In" in btn.text:
            self.safe_click(self.TOGGLE_MODE_BTN)
            time.sleep(0.3)
        return self

    def switch_to_register_mode(self):
        btn = self.wait_for_visible(self.TOGGLE_MODE_BTN)
        if "Need an account" in btn.text or "Register" in btn.text:
            self.safe_click(self.TOGGLE_MODE_BTN)
            time.sleep(0.3)
        return self

    def login(self, username, password):
        self.switch_to_login_mode()
        self.safe_send_keys(self.USERNAME_INPUT, username)
        self.safe_send_keys(self.PASSWORD_INPUT, password)
        self.safe_click(self.SUBMIT_BTN)
        time.sleep(1)
        return self

    def register(self, username, email, password):
        self.switch_to_register_mode()
        self.safe_send_keys(self.USERNAME_INPUT, username)
        if self.is_visible(self.EMAIL_INPUT, timeout=2):
            self.safe_send_keys(self.EMAIL_INPUT, email)
        self.safe_send_keys(self.PASSWORD_INPUT, password)
        self.safe_click(self.SUBMIT_BTN)
        time.sleep(1)
        return self

    def get_error_message(self):
        if self.is_visible(self.ERROR_BOX, timeout=3):
            return self.get_text(self.ERROR_BOX)
        return ""
