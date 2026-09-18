"""
ScholarPulse AI Studio - Document Upload Modal Page Object
==========================================================
Encapsulates file uploads (.pdf, .docx, .txt, .pptx), web URL/PDF ingestion,
title overrides, and progress validation.
"""

import os
import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class UploadModalPage(BasePage):
    """Page Object for Document & Research Ingestion Modal."""

    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//h3[contains(text(), 'Ingest') or contains(text(), 'Upload')]]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")
    
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    TITLE_INPUT = (By.XPATH, "//input[@placeholder='Custom paper title (optional)' or @placeholder='Paper title (optional)']")
    URL_TAB_BTN = (By.XPATH, "//button[contains(text(), 'Web / PDF URL') or contains(text(), 'URL')]")
    FILE_TAB_BTN = (By.XPATH, "//button[contains(text(), 'File Upload') or contains(text(), 'File')]")
    URL_INPUT = (By.XPATH, "//input[@placeholder='https://arxiv.org/pdf/...' or @type='url']")
    
    SUBMIT_BTN = (By.XPATH, "//button[contains(text(), 'Upload & Index') or contains(text(), 'Ingest Paper') or contains(text(), 'Ingest & Index')]")
    ERROR_BOX = (By.XPATH, "//div[contains(@class, 'bg-rose-500')]")

    def is_modal_open(self):
        return self.is_visible(self.MODAL_CONTAINER, timeout=3)

    def close_modal(self):
        if self.is_visible(self.CLOSE_BTN, timeout=2):
            self.safe_click(self.CLOSE_BTN)
            time.sleep(0.3)
        return self

    def upload_file(self, file_path, custom_title=None):
        abs_path = os.path.abspath(file_path)
        file_elem = self.wait_for_presence(self.FILE_INPUT)
        file_elem.send_keys(abs_path)
        
        if custom_title and self.is_visible(self.TITLE_INPUT, timeout=2):
            self.safe_send_keys(self.TITLE_INPUT, custom_title)
            
        self.safe_click(self.SUBMIT_BTN)
        time.sleep(2)
        return self

    def ingest_url(self, url, custom_title=None):
        if self.is_visible(self.URL_TAB_BTN, timeout=2):
            self.safe_click(self.URL_TAB_BTN)
            time.sleep(0.3)
            
        self.safe_send_keys(self.URL_INPUT, url)
        if custom_title and self.is_visible(self.TITLE_INPUT, timeout=2):
            self.safe_send_keys(self.TITLE_INPUT, custom_title)
            
        self.safe_click(self.SUBMIT_BTN)
        time.sleep(2)
        return self
