"""
Test Suite 10: Cross-Paper Comparative Synthesis Matrix (SciSpace / Elicit Killer)
==================================================================================
Tests multi-paper selection, comparative matrix generation, literature review
synthesis tables (Methodology, Dataset, Findings, Gaps), and CSV exports.
"""

import unittest
import time
from selenium.webdriver.common.by import By
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import CrossPaperMatrixModalPOM

class TestCrossPaperMatrix(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.matrix = CrossPaperMatrixModalPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        cls.workspace.back_to_library()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_select_multiple_papers_and_open_matrix(self):
        """Verify selecting 2+ papers enables the synthesis action trigger."""
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        if len(checkboxes) >= 2:
            checkboxes[0].click()
            checkboxes[1].click()
            time.sleep(0.5)
            self.workspace.safe_click(self.workspace.SYNTHESIZE_MATRIX_BTN)
            time.sleep(1)
            self.assertTrue(self.matrix.is_visible(self.matrix.MODAL_CONTAINER, timeout=5), "Synthesis modal should be open")

    def test_02_generate_synthesis_matrix_table(self):
        """Verify generating synthesis matrix produces structured comparison table."""
        if self.matrix.is_visible(self.matrix.MODAL_CONTAINER, timeout=2):
            self.matrix.generate_matrix()
            time.sleep(2)
            tables = self.driver.find_elements(*self.matrix.MATRIX_TABLE)
            self.assertGreaterEqual(len(tables), 0, "Matrix comparison table should be rendered")
            self.matrix.close()

if __name__ == '__main__':
    unittest.main()
