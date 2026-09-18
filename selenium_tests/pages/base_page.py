"""
ScholarPulse AI Studio - Base Page Object
========================================
Reusable core interactions, explicit waits, JavaScript helpers,
DOM inspectors, and automated screenshot captures.
"""

import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)
from selenium_tests.config import EXPLICIT_WAIT, POLL_FREQUENCY, SCREENSHOTS_DIR

class BasePage:
    """Base class for all Page Object Models."""

    def __init__(self, driver, base_url=None):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT, poll_frequency=POLL_FREQUENCY)

    def open(self, path=""):
        url = f"{self.base_url}{path}" if self.base_url else path
        self.driver.get(url)
        return self

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def wait_for_visible(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT, poll_frequency=POLL_FREQUENCY)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT, poll_frequency=POLL_FREQUENCY)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT, poll_frequency=POLL_FREQUENCY)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_invisibility(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT, poll_frequency=POLL_FREQUENCY)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text(self, locator, text, timeout=None):
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT, poll_frequency=POLL_FREQUENCY)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_present(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def safe_click(self, locator, timeout=None):
        try:
            element = self.wait_for_clickable(locator, timeout=timeout)
            self.scroll_into_view(element)
            element.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            # Fallback: JavaScript Click
            element = self.wait_for_presence(locator, timeout=timeout)
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def safe_send_keys(self, locator, text, clear_first=True, timeout=None):
        element = self.wait_for_visible(locator, timeout=timeout)
        self.scroll_into_view(element)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator, timeout=None):
        element = self.wait_for_visible(locator, timeout=timeout)
        return element.text.strip()

    def get_attribute(self, locator, attribute_name, timeout=None):
        element = self.wait_for_presence(locator, timeout=timeout)
        return element.get_attribute(attribute_name)

    def scroll_into_view(self, element_or_locator):
        if isinstance(element_or_locator, tuple):
            element = self.find_element(element_or_locator)
        else:
            element = element_or_locator
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def take_screenshot(self, name_prefix="screenshot"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_prefix = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name_prefix)
        filename = f"{safe_prefix}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath

    def wait_for_ajax_or_dom_ready(self, timeout=10):
        """Wait until document.readyState == 'complete' and fetch/XHR operations idle."""
        start = time.time()
        while time.time() - start < timeout:
            ready_state = self.driver.execute_script("return document.readyState;")
            if ready_state == "complete":
                break
            time.sleep(0.2)
