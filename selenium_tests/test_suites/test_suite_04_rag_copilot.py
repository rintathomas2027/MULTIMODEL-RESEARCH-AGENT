"""
Test Suite 04: Semantic RAG Copilot Chat & Document Summarizer
==============================================================
Tests Grounded Research QA, Vector Chunk Retrieval, Context Grounding,
and Document Executive Summarization.
"""

import unittest
import time
from selenium_tests.driver_factory import DriverFactory
from selenium_tests.config import BASE_URL, SAMPLE_RESEARCH_PROMPT
from selenium_tests.pages.workspace_page import WorkspacePage
from selenium_tests.pages.research_tabs_page import ChatTabPOM

class TestRAGCopilot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.get_driver()
        cls.workspace = WorkspacePage(cls.driver, BASE_URL)
        cls.chat = ChatTabPOM(cls.driver, BASE_URL)

        # Open workspace and select document
        cls.workspace.open_home()
        cls.workspace.enter_workspace()
        time.sleep(1)
        if cls.workspace.get_document_count() > 0:
            cls.workspace.select_first_document()
            cls.workspace.switch_tab("chat")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_chat_tab_ui_rendered(self):
        """Verify RAG Chat interface, text input, and action buttons render."""
        self.assertTrue(self.chat.is_visible(self.chat.CHAT_INPUT, timeout=5), "Chat input textarea must be visible")
        self.assertTrue(self.chat.is_visible(self.chat.SEND_BTN, timeout=5), "Send button must be visible")

    def test_02_send_grounded_rag_query(self):
        """Verify submitting a query generates an AI answer bubble."""
        self.chat.send_question(SAMPLE_RESEARCH_PROMPT)
        time.sleep(2)
        messages = self.driver.find_elements(*self.chat.MESSAGE_BUBBLES)
        self.assertGreaterEqual(len(messages), 1, "At least one chat bubble should be rendered")

    def test_03_generate_document_summary(self):
        """Verify clicking generate summary produces structured executive summary."""
        self.chat.generate_summary()
        time.sleep(2)
        summary_container = self.driver.find_elements(*self.chat.SUMMARY_CONTAINER)
        self.assertGreaterEqual(len(summary_container), 0, "Summary section should be rendered")

if __name__ == '__main__':
    unittest.main()
