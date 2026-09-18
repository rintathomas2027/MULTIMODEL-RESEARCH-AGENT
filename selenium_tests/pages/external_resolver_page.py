"""
ScholarPulse AI Studio - DOI / ArXiv External Resolver Page Object
==================================================================
Handles 1-Click external paper resolution via CrossRef and arXiv APIs,
metadata review, and auto-importing to the user library.
"""

import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ExternalResolverPage(BasePage):
    """Page Object for DOI / ArXiv 1-Click Resolver Modal."""

    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//h3[contains(text(), 'DOI') or contains(text(), 'arXiv')]]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")
    
    IDENTIFIER_INPUT = (By.XPATH, "//input[@placeholder='e.g. 10.1145/3372278.3390670 or 1706.03762' or contains(@placeholder, '10.')]")
    RESOLVE_BTN = (By.XPATH, "//button[contains(text(), 'Resolve & Import') or contains(text(), 'Resolve Paper') or contains(text(), 'Fetch')]")
    RESOLVED_CARD = (By.XPATH, "//div[contains(@class, 'glass-card') and .//h4]")
    ERROR_BOX = (By.XPATH, "//div[contains(@class, 'bg-rose-500')]")

    def is_modal_open(self):
        return self.is_visible(self.MODAL_CONTAINER, timeout=3)

    def close_modal(self):
        if self.is_visible(self.CLOSE_BTN, timeout=2):
            self.safe_click(self.CLOSE_BTN)
            time.sleep(0.3)
        return self

    def resolve_paper(self, identifier):
        self.safe_send_keys(self.IDENTIFIER_INPUT, identifier)
        self.safe_click(self.RESOLVE_BTN)
        time.sleep(3)
        return self

    def get_error_message(self):
        if self.is_visible(self.ERROR_BOX, timeout=3):
            return self.get_text(self.ERROR_BOX)
        return ""
