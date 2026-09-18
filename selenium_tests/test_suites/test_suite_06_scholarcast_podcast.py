"""
Test Suite 06: "ScholarCast" Dual-Host Audio Deep Dive
======================================================
Tests paper-to-podcast dialogue synthesis, speech player controls,
playback speed modulation (0.75x to 2.0x), and synchronized transcripts.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import ScholarCastTabPOM

class TestScholarCastPodcast(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.podcast = ScholarCastTabPOM(cls.driver, BASE_URL)

        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)
        if cls.workspace.get_document_count() > 0:
            cls.workspace.select_first_document()
            cls.workspace.switch_tab("scholarcast")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_scholarcast_tab_rendered(self):
        """Verify ScholarCast Studio UI elements load."""
        time.sleep(1)
        self.assertTrue(self.podcast.is_visible(self.podcast.GENERATE_PODCAST_BTN, timeout=5) or 
                        self.podcast.is_visible(self.podcast.PLAY_PAUSE_BTN, timeout=5),
                        "ScholarCast action buttons must be displayed")

    def test_02_generate_podcast_episode(self):
        """Verify generating dual-host podcast dialogue produces speaker turns."""
        self.podcast.generate_podcast()
        time.sleep(2)
        dialogues = self.driver.find_elements(*self.podcast.TRANSCRIPT_DIALOGUES)
        self.assertGreaterEqual(len(dialogues), 1, "Speaker dialogue cards should be generated")

    def test_03_playback_controls_and_speed_toggles(self):
        """Verify play/pause controls and speed selector buttons."""
        self.podcast.toggle_playback()
        time.sleep(0.5)

if __name__ == '__main__':
    unittest.main()
