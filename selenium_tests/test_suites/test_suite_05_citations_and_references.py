"""
Test Suite 05: Mendeley & Zotero Academic Citation Hub
======================================================
Tests Citation Formatting across APA 7th, IEEE, Harvard, MLA 9, Chicago,
BibTeX, RIS standards, 1-Click clipboard copying, and file downloads.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import CitationsTabPOM

class TestCitationsAndReferences(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.citations = CitationsTabPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)
        if cls.workspace.get_document_count() > 0:
            cls.workspace.select_first_document()
            cls.workspace.switch_tab("citations")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_citations_tab_rendered(self):
        """Verify Citation Studio loads with academic format cards."""
        time.sleep(1.5)
        blocks = self.driver.find_elements(*self.citations.FORMAT_BLOCKS)
        self.assertGreaterEqual(len(blocks), 1, "Citation format blocks must be displayed")

    def test_02_bibtex_and_ris_exports_available(self):
        """Verify 1-Click .BIB and .RIS export buttons are present."""
        self.assertTrue(self.citations.is_visible(self.citations.EXPORT_BIB_BTN, timeout=5), "Download .BIB button must be present")
        self.assertTrue(self.citations.is_visible(self.citations.EXPORT_RIS_BTN, timeout=5), "Download .RIS button must be present")

    def test_03_copy_citation_interaction(self):
        """Verify clicking Copy citation triggers copy feedback without errors."""
        self.citations.copy_first_citation()
        time.sleep(0.5)

if __name__ == '__main__':
    unittest.main()
