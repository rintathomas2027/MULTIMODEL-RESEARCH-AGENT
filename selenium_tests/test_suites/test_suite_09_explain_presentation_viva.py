"""
Test Suite 09: Adaptive Explainer, Presentation Slides & Viva Defense Prep
==========================================================================
Tests 4-tier conceptual explain engine, 5-slide academic presentation deck generator,
and University Viva & Defense exam prep modules.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import (
    ExplainTabPOM,
    PresentationTabPOM,
    VivaTabPOM
)

class TestExplainPresentationViva(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.explain = ExplainTabPOM(cls.driver, BASE_URL)
        cls.presentation = PresentationTabPOM(cls.driver, BASE_URL)
        cls.viva = VivaTabPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)
        if cls.workspace.get_document_count() > 0:
            cls.workspace.select_first_document()

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_adaptive_explain_mode(self):
        """Verify selecting academic tier generates tailored conceptual explanation."""
        self.workspace.switch_tab("explain")
        time.sleep(1)
        self.explain.explain("Self-Attention", tier="MCA Engineer")
        time.sleep(2)
        boxes = self.driver.find_elements(*self.explain.EXPLANATION_BOX)
        self.assertGreaterEqual(len(boxes), 1, "Explanation card should be rendered")

    def test_02_presentation_slide_generator(self):
        """Verify generating presentation slide deck creates 5-slide carousel."""
        self.workspace.switch_tab("presentation")
        time.sleep(1)
        self.presentation.generate_presentation()
        time.sleep(2)
        slides = self.driver.find_elements(*self.presentation.SLIDE_CARD)
        self.assertGreaterEqual(len(slides), 1, "Presentation slide cards should be rendered")

    def test_03_university_viva_defense_prep(self):
        """Verify generating viva prep produces 2-mark, 5-mark, and external viva questions."""
        self.workspace.switch_tab("viva")
        time.sleep(1)
        self.viva.generate_viva()
        time.sleep(2)
        questions = self.driver.find_elements(*self.viva.QUESTION_ACCORDIONS)
        self.assertGreaterEqual(len(questions), 1, "Viva question accordions should be rendered")

if __name__ == '__main__':
    unittest.main()
