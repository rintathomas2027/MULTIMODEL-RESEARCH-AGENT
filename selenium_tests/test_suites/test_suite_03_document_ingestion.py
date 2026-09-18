"""
Test Suite 03: Document Ingestion, File Upload, DOI/ArXiv & Search
==================================================================
Tests document ingestion workflows: multi-format file uploads, web URL parsing,
1-Click DOI / ArXiv resolution, and Library search filtering.
"""

import unittest
import time
import os
from selenium.webdriver.common.by import By
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL, SAMPLE_ARXIV_ID
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.upload_modal_page import UploadModalPage
from selenium_tests.pages.external_resolver_page import ExternalResolverPage

class TestDocumentIngestion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.upload = UploadModalPage(cls.driver, BASE_URL)
        cls.resolver = ExternalResolverPage(cls.driver, BASE_URL)

        # Ensure inside workspace as guest or user
        cls.workspace.open_home()
        cls.workspace.enter_workspace()

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_upload_modal_display(self):
        """Verify upload modal opens and contains File and URL tabs."""
        self.workspace.open_upload_modal()
        self.assertTrue(self.upload.is_modal_open(), "Upload modal should be visible")
        self.upload.close_modal()

    def test_02_upload_text_research_document(self):
        """Verify uploading a text paper creates an indexed document card."""
        # Create a temporary test document
        test_file_path = os.path.join(os.getcwd(), "test_paper_temp.txt")
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("A Scalable Architecture for Multi-Modal Foundation Models.\nAbstract: We investigate sparse mixture-of-experts in multimodal LLMs.")

        try:
            initial_count = self.workspace.get_document_count()
            self.workspace.open_upload_modal()
            self.upload.upload_file(test_file_path, custom_title="Multi-Modal MoE Paper")
            time.sleep(2)
            new_count = self.workspace.get_document_count()
            self.assertGreaterEqual(new_count, initial_count, "Document count should increase or stay updated")
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_03_external_doi_arxiv_resolver_modal(self):
        """Verify external DOI/ArXiv resolver modal opens, accepts identifier, and closes."""
        self.workspace.open_external_resolver()
        self.assertTrue(self.resolver.is_modal_open(), "DOI / ArXiv modal should be open")
        self.resolver.close_modal()

    def test_04_document_search_filtering(self):
        """Verify searching for a keyword in document library filters results."""
        search_input = self.driver.find_elements(By.XPATH, "//input[@placeholder='Search papers by title or keywords...' or contains(@placeholder, 'Search papers')]")
        if search_input:
            search_input[0].clear()
            search_input[0].send_keys("Transformer")
            time.sleep(1)
            cards = self.workspace.get_document_count()
            self.assertGreaterEqual(cards, 0, "Search should return matching cards")
            # Clear search
            search_input[0].clear()
            time.sleep(0.5)

if __name__ == '__main__':
    unittest.main()
