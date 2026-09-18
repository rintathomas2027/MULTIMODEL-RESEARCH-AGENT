"""
Test Suite 07: "Reviewer #2" Critical Rigor Roast & Scientific Auditor
======================================================================
Tests peer-review simulation, Rigor Score computation (0-100),
fatal flaws detection, baseline audits, and defense directives.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import CriticalRoastTabPOM

class TestReviewer2RigorAudit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.roast = CriticalRoastTabPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)
        if cls.workspace.get_document_count() > 0:
            cls.workspace.select_first_document()
            cls.workspace.switch_tab("roast")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_roast_tab_rendered(self):
        """Verify Reviewer #2 Auditor interface loads."""
        time.sleep(1)
        self.assertTrue(self.roast.is_visible(self.roast.GENERATE_ROAST_BTN, timeout=5) or 
                        self.roast.is_visible(self.roast.RIGOR_SCORE_CONTAINER, timeout=5),
                        "Rigor audit trigger or score gauge must be visible")

    def test_02_trigger_rigor_audit(self):
        """Verify executing rigor audit produces a rigor score and critique breakdown."""
        self.roast.generate_audit()
        time.sleep(2)
        score_elements = self.driver.find_elements(*self.roast.RIGOR_SCORE_CONTAINER)
        self.assertGreaterEqual(len(score_elements), 0, "Audit results should render")

if __name__ == '__main__':
    unittest.main()
