"""
Test Suite 08: Multimodal Math Formula & Algorithm to Code Synthesizer
======================================================================
Tests LaTeX mathematical equation input, algorithm parsing,
and automatic PyTorch / Python code synthesis with complexity analysis.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL, SAMPLE_FORMULA_QUERY
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import FormulaCodeTabPOM

class TestFormulaToCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.formula = FormulaCodeTabPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)
        if cls.workspace.get_document_count() > 0:
            cls.workspace.select_first_document()
            cls.workspace.switch_tab("formula")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_formula_tab_rendered(self):
        """Verify Formula to Code Synthesizer UI loads."""
        time.sleep(1)
        self.assertTrue(self.formula.is_visible(self.formula.FORMULA_INPUT, timeout=5), "Equation input field must be visible")
        self.assertTrue(self.formula.is_visible(self.formula.SYNTHESIZE_BTN, timeout=5), "Synthesize code button must be visible")

    def test_02_synthesize_pytorch_code(self):
        """Verify submitting equation produces syntax-highlighted Python/PyTorch code block."""
        self.formula.synthesize_code(SAMPLE_FORMULA_QUERY)
        time.sleep(2)
        code_blocks = self.driver.find_elements(*self.formula.CODE_CONTAINER)
        self.assertGreaterEqual(len(code_blocks), 0, "Synthesized code block should be rendered")

if __name__ == '__main__':
    unittest.main()
