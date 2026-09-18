"""
ScholarPulse AI Studio - Cross-Browser WebDriver Factory
=======================================================
Initializes robust, cross-platform WebDrivers for Google Chrome,
Microsoft Edge, and Mozilla Firefox with headless support and resilient options.
"""

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from .config import (
    DEFAULT_BROWSER,
    HEADLESS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PAGE_LOAD_TIMEOUT,
    IMPLICIT_WAIT
)

class DriverFactory:
    """Factory class to create configured WebDriver instances."""

    @staticmethod
    def get_driver(browser_name=None, headless=None):
        browser = (browser_name or DEFAULT_BROWSER).lower()
        is_headless = HEADLESS if headless is None else headless

        driver = None

        if browser in ("chrome", "google-chrome", "chromium"):
            driver = DriverFactory._create_chrome_driver(is_headless)
        elif browser in ("edge", "msedge", "microsoftedge"):
            driver = DriverFactory._create_edge_driver(is_headless)
        elif browser in ("firefox", "gecko", "mozilla"):
            driver = DriverFactory._create_firefox_driver(is_headless)
        else:
            # Default to Chrome
            try:
                driver = DriverFactory._create_chrome_driver(is_headless)
            except Exception:
                # Fallback to Edge on Windows
                driver = DriverFactory._create_edge_driver(is_headless)

        # Configure universal timeouts and window parameters
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(IMPLICIT_WAIT)
        try:
            driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        except Exception:
            pass

        return driver

    @staticmethod
    def _create_chrome_driver(headless=True):
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        except Exception:
            # Fallback to PATH or Selenium Manager
            return webdriver.Chrome(options=options)

    @staticmethod
    def _create_edge_driver(headless=True):
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
        options.add_argument("--disable-blink-features=AutomationControlled")

        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)
        except Exception:
            return webdriver.Edge(options=options)

    @staticmethod
    def _create_firefox_driver(headless=True):
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.add_argument(f"--width={WINDOW_WIDTH}")
        options.add_argument(f"--height={WINDOW_HEIGHT}")

        try:
            from webdriver_manager.firefox import GeckoDriverManager
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        except Exception:
            return webdriver.Firefox(options=options)
