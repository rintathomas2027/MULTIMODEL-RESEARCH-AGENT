"""
ScholarPulse AI Studio - Workspace Page Object
==============================================
Encapsulates workspace interactions, header controls, theme switching,
document listing, search filter, and quick tool triggers.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage

class WorkspacePage(BasePage):
    """Page Object for ScholarPulse Research Studio & Workspace."""

    # Locators
    ROOT_CONTAINER = (By.ID, "root")
    LOGO = (By.XPATH, "//div[contains(text(), '⚡')]/..")
    THEME_TOGGLE_BTN = (By.XPATH, "//button[@title='Toggle Theme']")
    ENTER_WORKSPACE_BTN = (By.XPATH, "//button[contains(text(), 'Continue to Workspace') or contains(text(), 'Launch Research Workspace') or contains(text(), 'Go to Workspace')]")
    GUEST_ACCESS_BTN = (By.XPATH, "//button[contains(text(), '1-Click Access') or contains(text(), '1-Click Instant Guest')]")
    SIGN_IN_REGISTER_BTN = (By.XPATH, "//button[contains(text(), 'Sign In / Register')]")
    UPLOAD_MODAL_BTN = (By.XPATH, "//button[contains(., 'Upload')]")
    EXTERNAL_RESOLVER_BTN = (By.XPATH, "//button[contains(., 'DOI / arXiv') or contains(., 'Ingest DOI')]")
    CMD_K_BAR = (By.XPATH, "//div[contains(., 'Search or command')]")
    ANALYTICS_TRIGGER = (By.XPATH, "//div[contains(@title, 'Analytics') or contains(., 'XP • Lvl')]")
    FEEDBACK_TRIGGER = (By.XPATH, "//button[contains(@title, 'Satisfaction') or contains(., 'Rate App')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(@title, 'Log Out') or contains(., 'Log Out')]")

    # Document Library
    DOC_CARDS = (By.XPATH, "//div[contains(@class, 'glass-card') and .//h3]")
    FIRST_DOC_CARD = (By.XPATH, "(//div[contains(@class, 'glass-card') and .//h3])[1]")
    SYNTHESIZE_MATRIX_BTN = (By.XPATH, "//button[contains(., 'Synthesize') and contains(., 'Papers')]")

    # Studio Workbench
    BACK_TO_LIBRARY_BTN = (By.XPATH, "//button[contains(text(), '← Back')]")
    STUDIO_HEADER_TITLE = (By.XPATH, "//main//h2")
    TAB_CHAT = (By.XPATH, "//button[@data-tab='chat']")
    TAB_CITATIONS = (By.XPATH, "//button[@data-tab='citations']")
    TAB_SCHOLARCAST = (By.XPATH, "//button[@data-tab='scholarcast']")
    TAB_ROAST = (By.XPATH, "//button[@data-tab='roast']")
    TAB_FORMULA = (By.XPATH, "//button[@data-tab='formula']")
    TAB_EXPLAIN = (By.XPATH, "//button[@data-tab='explain']")
    TAB_PRESENTATION = (By.XPATH, "//button[@data-tab='presentation']")
    TAB_VIVA = (By.XPATH, "//button[@data-tab='viva']")

    def open_home(self):
        self.open("/")
        self.wait_for_presence(self.ROOT_CONTAINER)
        return self

    def toggle_theme(self):
        self.safe_click(self.THEME_TOGGLE_BTN)
        time.sleep(0.3)
        html_class = self.driver.find_element(By.TAG_NAME, "html").get_attribute("class")
        return "dark" if "dark" in html_class else "light"

    def enter_workspace(self):
        if self.is_visible(self.ENTER_WORKSPACE_BTN, timeout=3):
            self.safe_click(self.ENTER_WORKSPACE_BTN)
            time.sleep(0.5)
        elif self.is_visible(self.GUEST_ACCESS_BTN, timeout=2):
            self.safe_click(self.GUEST_ACCESS_BTN)
            time.sleep(0.5)
        return self

    def open_auth_modal(self):
        self.safe_click(self.SIGN_IN_REGISTER_BTN)
        return self

    def open_upload_modal(self):
        self.safe_click(self.UPLOAD_MODAL_BTN)
        return self

    def open_external_resolver(self):
        self.safe_click(self.EXTERNAL_RESOLVER_BTN)
        return self

    def open_command_hub(self):
        # Trigger via clicking search bar or via Ctrl+K
        if self.is_visible(self.CMD_K_BAR, timeout=2):
            self.safe_click(self.CMD_K_BAR)
        else:
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('k').key_up(Keys.CONTROL).perform()
        time.sleep(0.4)
        return self

    def get_document_count(self):
        cards = self.find_elements(self.DOC_CARDS)
        return len(cards)

    def select_first_document(self):
        self.safe_click(self.FIRST_DOC_CARD)
        time.sleep(0.5)
        return self

    def switch_tab(self, tab_name):
        tab_locators = {
            "chat": self.TAB_CHAT,
            "citations": self.TAB_CITATIONS,
            "scholarcast": self.TAB_SCHOLARCAST,
            "roast": self.TAB_ROAST,
            "formula": self.TAB_FORMULA,
            "explain": self.TAB_EXPLAIN,
            "presentation": self.TAB_PRESENTATION,
            "viva": self.TAB_VIVA,
        }
        loc = tab_locators.get(tab_name.lower())
        if loc:
            self.safe_click(loc)
            time.sleep(0.4)
        return self

    def back_to_library(self):
        if self.is_visible(self.BACK_TO_LIBRARY_BTN, timeout=3):
            self.safe_click(self.BACK_TO_LIBRARY_BTN)
            time.sleep(0.4)
        return self

    def logout(self):
        if self.is_visible(self.LOGOUT_BTN, timeout=3):
            self.safe_click(self.LOGOUT_BTN)
            time.sleep(0.5)
        return self
