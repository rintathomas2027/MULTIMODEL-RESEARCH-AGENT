"""
ScholarPulse AI Studio - Research Tabs & Interactive Modules Page Object
========================================================================
Encapsulates all 14 cutting-edge modules:
1. RAG Copilot Chat & Summarizer
2. Mendeley / Zotero Citations Hub (APA, IEEE, Harvard, BibTeX, RIS)
3. ScholarCast Dual-Host Audio Deep Dive
4. Reviewer #2 Critical Rigor Roast & Auditor
5. Multimodal Formula to PyTorch/Python Code Synthesizer
6. Adaptive 4-Level Explain Engine
7. Presentation Slide Deck Generator
8. University Viva & Defense Exam Prep
9. Cross-Paper Comparative Synthesis Matrix
10. Research Analytics & Gamification Hub
11. User Satisfaction Feedback Modal
"""

import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ChatTabPOM(BasePage):
    """RAG Copilot Chat Tab."""
    CHAT_INPUT = (By.XPATH, "//textarea[@placeholder='Ask grounded questions about this research paper...' or contains(@placeholder, 'Ask')]")
    SEND_BTN = (By.XPATH, "//button[contains(., 'Send Query') or contains(., 'Ask') or contains(., 'Send')]")
    MESSAGE_BUBBLES = (By.XPATH, "//div[contains(@class, 'glass-card') and (.//p or .//div)]")
    GENERATE_SUMMARY_BTN = (By.XPATH, "//button[contains(text(), 'Detailed Executive Summary') or contains(text(), 'Generate Full Summary') or contains(text(), 'Generate')]")
    SUMMARY_CONTAINER = (By.XPATH, "//div[contains(@class, 'prose') or contains(@class, 'summary-text')]")

    def send_question(self, question):
        self.safe_send_keys(self.CHAT_INPUT, question)
        self.safe_click(self.SEND_BTN)
        time.sleep(3)
        return self

    def generate_summary(self):
        if self.is_visible(self.GENERATE_SUMMARY_BTN, timeout=3):
            self.safe_click(self.GENERATE_SUMMARY_BTN)
            time.sleep(3)
        return self


class CitationsTabPOM(BasePage):
    """Mendeley & Zotero Citation Hub Tab."""
    BIBTEX_BOX = (By.XPATH, "//pre[contains(text(), '@article') or contains(text(), '@')]")
    COPY_BUTTONS = (By.XPATH, "//button[contains(text(), 'Copy') or contains(., '📋')]")
    EXPORT_BIB_BTN = (By.XPATH, "//button[contains(., 'Download .BIB') or contains(., 'Export .bib')]")
    EXPORT_RIS_BTN = (By.XPATH, "//button[contains(., 'Download .RIS') or contains(., 'Export .ris')]")
    FORMAT_BLOCKS = (By.XPATH, "//div[contains(@class, 'glass-card') and (.//h4 or .//span)]")

    def copy_first_citation(self):
        btns = self.find_elements(self.COPY_BUTTONS)
        if btns:
            btns[0].click()
            time.sleep(0.3)
        return self


class ScholarCastTabPOM(BasePage):
    """ScholarCast Dual-Host Audio Deep Dive Tab."""
    GENERATE_PODCAST_BTN = (By.XPATH, "//button[contains(., 'Synthesize Dual-Host Audio') or contains(., 'Generate Podcast') or contains(., 'Generate')]")
    PLAY_PAUSE_BTN = (By.XPATH, "//button[contains(., 'Play Episode') or contains(., 'Pause Episode') or contains(., '▶') or contains(., '⏸')]")
    SPEED_BTNS = (By.XPATH, "//button[contains(text(), '1.0x') or contains(text(), '1.25x') or contains(text(), '1.5x')]")
    TRANSCRIPT_DIALOGUES = (By.XPATH, "//div[contains(@class, 'p-4 rounded-2xl') or contains(@class, 'glass-card')]")

    def generate_podcast(self):
        if self.is_visible(self.GENERATE_PODCAST_BTN, timeout=3):
            self.safe_click(self.GENERATE_PODCAST_BTN)
            time.sleep(3)
        return self

    def toggle_playback(self):
        if self.is_visible(self.PLAY_PAUSE_BTN, timeout=3):
            self.safe_click(self.PLAY_PAUSE_BTN)
            time.sleep(0.5)
        return self


class CriticalRoastTabPOM(BasePage):
    """Reviewer #2 Critical Rigor Auditor Tab."""
    GENERATE_ROAST_BTN = (By.XPATH, "//button[contains(., 'Audit Rigor') or contains(., 'Generate Rigor Audit') or contains(., 'Analyze')]")
    RIGOR_SCORE_CONTAINER = (By.XPATH, "//div[contains(@class, 'text-4xl') or contains(text(), 'Rigor Score') or contains(text(), '/100')]")
    FLAWS_LIST = (By.XPATH, "//div[contains(@class, 'border-rose-500') or contains(@class, 'bg-rose-500')]")

    def generate_audit(self):
        if self.is_visible(self.GENERATE_ROAST_BTN, timeout=3):
            self.safe_click(self.GENERATE_ROAST_BTN)
            time.sleep(3)
        return self


class FormulaCodeTabPOM(BasePage):
    """Multimodal Formula to PyTorch/Python Code Synthesizer Tab."""
    FORMULA_INPUT = (By.XPATH, "//textarea[contains(@placeholder, 'Target equation') or contains(@placeholder, 'equation') or contains(@placeholder, 'formula')]")
    SYNTHESIZE_BTN = (By.XPATH, "//button[contains(., 'Synthesize Implementation') or contains(., 'Convert to Code') or contains(., 'Generate Code')]")
    CODE_CONTAINER = (By.XPATH, "//pre[contains(@class, 'font-mono')]//code")

    def synthesize_code(self, formula_text):
        self.safe_send_keys(self.FORMULA_INPUT, formula_text)
        self.safe_click(self.SYNTHESIZE_BTN)
        time.sleep(3)
        return self


class ExplainTabPOM(BasePage):
    """Adaptive 4-Level Explain Engine Tab."""
    TIER_BUTTONS = (By.XPATH, "//button[contains(text(), 'Beginner') or contains(text(), 'Undergraduate') or contains(text(), 'MCA') or contains(text(), 'Scholar')]")
    CONCEPT_INPUT = (By.XPATH, "//input[@placeholder='Specific concept to explain (e.g. Backpropagation, Attention)' or @type='text']")
    EXPLAIN_BTN = (By.XPATH, "//button[contains(., 'Generate Tailored Explanation') or contains(., 'Explain Concept')]")
    EXPLANATION_BOX = (By.XPATH, "//div[contains(@class, 'glass-card') and .//p]")

    def explain(self, concept="Self Attention Mechanism", tier="MCA Engineer"):
        if self.is_visible(self.CONCEPT_INPUT, timeout=2):
            self.safe_send_keys(self.CONCEPT_INPUT, concept)
        tier_btn = (By.XPATH, f"//button[contains(text(), '{tier}')]")
        if self.is_visible(tier_btn, timeout=2):
            self.safe_click(tier_btn)
        self.safe_click(self.EXPLAIN_BTN)
        time.sleep(3)
        return self


class PresentationTabPOM(BasePage):
    """Presentation Slide Deck Generator Tab."""
    GENERATE_SLIDES_BTN = (By.XPATH, "//button[contains(., 'Generate 5-Slide Presentation') or contains(., 'Generate Deck') or contains(., 'Generate Slides')]")
    SLIDE_CARD = (By.XPATH, "//div[contains(@class, 'glass-card') and (.//h2 or .//h3)]")
    NEXT_SLIDE_BTN = (By.XPATH, "//button[contains(text(), 'Next Slide') or contains(text(), '→')]")
    PREV_SLIDE_BTN = (By.XPATH, "//button[contains(text(), 'Previous Slide') or contains(text(), '←')]")

    def generate_presentation(self):
        if self.is_visible(self.GENERATE_SLIDES_BTN, timeout=3):
            self.safe_click(self.GENERATE_SLIDES_BTN)
            time.sleep(3)
        return self


class VivaTabPOM(BasePage):
    """University Viva & Defense Exam Prep Tab."""
    GENERATE_VIVA_BTN = (By.XPATH, "//button[contains(., 'Generate Complete Viva Prep') or contains(., 'Generate Viva') or contains(., 'Start Defense Prep')]")
    QUESTION_ACCORDIONS = (By.XPATH, "//div[contains(@class, 'glass-card') and (.//span or .//h4)]")

    def generate_viva(self):
        if self.is_visible(self.GENERATE_VIVA_BTN, timeout=3):
            self.safe_click(self.GENERATE_VIVA_BTN)
            time.sleep(3)
        return self


class CrossPaperMatrixModalPOM(BasePage):
    """Cross-Paper Comparative Synthesis Matrix Modal."""
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//h3[contains(text(), 'Synthesis') or contains(text(), 'Matrix')]]")
    GENERATE_MATRIX_BTN = (By.XPATH, "//button[contains(., 'Synthesize Matrix') or contains(., 'Generate Literature Matrix')]")
    MATRIX_TABLE = (By.XPATH, "//table")
    EXPORT_CSV_BTN = (By.XPATH, "//button[contains(., 'Download Matrix CSV') or contains(., 'Export CSV')]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")

    def generate_matrix(self):
        if self.is_visible(self.GENERATE_MATRIX_BTN, timeout=3):
            self.safe_click(self.GENERATE_MATRIX_BTN)
            time.sleep(3)
        return self

    def close(self):
        if self.is_visible(self.CLOSE_BTN, timeout=2):
            self.safe_click(self.CLOSE_BTN)
            time.sleep(0.3)
        return self


class AnalyticsModalPOM(BasePage):
    """Research Analytics & Gamification Modal."""
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//h3[contains(text(), 'Analytics') or contains(text(), 'Research')]]")
    XP_BADGE = (By.XPATH, "//div[contains(text(), 'XP') or contains(text(), 'Level')]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")

    def close(self):
        if self.is_visible(self.CLOSE_BTN, timeout=2):
            self.safe_click(self.CLOSE_BTN)
            time.sleep(0.3)
        return self


class FeedbackModalPOM(BasePage):
    """User Satisfaction Feedback Modal."""
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class, 'fixed inset-0') and .//h3[contains(text(), 'Satisfaction') or contains(text(), 'Feedback')]]")
    STAR_BTNS = (By.XPATH, "//button[contains(text(), '★') or contains(., '★')]")
    COMMENT_INPUT = (By.XPATH, "//textarea[@placeholder='What did you enjoy most, or what features should we add next?' or contains(@class, 'rounded-xl')]")
    SUBMIT_FEEDBACK_BTN = (By.XPATH, "//button[contains(text(), 'Submit Evaluation & Claim') or contains(text(), 'Submit Feedback')]")
    CLOSE_BTN = (By.XPATH, "//div[contains(@class, 'fixed inset-0')]//button[contains(text(), '✕')]")

    def submit_rating(self, stars=5, comment="Exceptional multimodal AI research platform!"):
        stars_elems = self.find_elements(self.STAR_BTNS)
        if stars_elems and len(stars_elems) >= stars:
            stars_elems[stars - 1].click()
        if self.is_visible(self.COMMENT_INPUT, timeout=2):
            self.safe_send_keys(self.COMMENT_INPUT, comment)
        self.safe_click(self.SUBMIT_FEEDBACK_BTN)
        time.sleep(0.5)
        return self
