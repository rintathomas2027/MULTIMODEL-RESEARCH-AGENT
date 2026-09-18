"""
ScholarPulse AI Studio - Universal Command Hub (Ctrl+K) Page Object
===================================================================
Spotlight-style command palette for quick tool triggers, document jumping,
theme toggles, and shortcuts.
"""

import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CommandHubPage(BasePage):
    """Page Object for Spotlight Command Hub (Ctrl+K)."""

    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//input[contains(@placeholder, 'Type a command') or contains(@placeholder, 'search')]]")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Type a command') or contains(@placeholder, 'Search')]")
    COMMAND_ITEMS = (By.XPATH, "//div[contains(@class, 'cursor-pointer') and .//span]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕') or contains(text(), 'ESC')]")

    def is_hub_open(self):
        return self.is_visible(self.MODAL_CONTAINER, timeout=3)

    def search_and_select(self, command_text):
        self.safe_send_keys(self.SEARCH_INPUT, command_text)
        time.sleep(0.3)
        item_xpath = f"//div[contains(@class, 'cursor-pointer') and contains(., '{command_text}')]"
        self.safe_click((By.XPATH, item_xpath))
        time.sleep(0.5)
        return self
