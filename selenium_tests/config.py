"""
ScholarPulse AI Studio - Selenium Automation Test Configuration
===============================================================
Central configuration module for WebDriver options, target URLs,
timeouts, test credentials, and reporting directories.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

# Ensure output directories exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Test Target Server
BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:8000")
API_BASE_URL = f"{BASE_URL}/api"

# Browser & Driver Settings
DEFAULT_BROWSER = os.getenv("TEST_BROWSER", "chrome").lower()  # 'chrome', 'edge', 'firefox'
HEADLESS = os.getenv("TEST_HEADLESS", "true").lower() in ("true", "1", "yes")
WINDOW_WIDTH = int(os.getenv("TEST_WINDOW_WIDTH", "1920"))
WINDOW_HEIGHT = int(os.getenv("TEST_WINDOW_HEIGHT", "1080"))

# Timeouts (seconds)
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 15
POLL_FREQUENCY = 0.5

# Test User Credentials
TEST_USER = {
    "username": "scholar_tester",
    "email": "tester@scholarpulse.ai",
    "password": "ValidPassword@2026",
    "academic_level": "MCA Student",
    "avatar": "technomancer"
}

DEMO_USER = {
    "username": "MCA_Evaluator",
    "password": "Research@2026"
}

# Test Data Constants
SAMPLE_DOI = "10.1145/3372278.3390670"
SAMPLE_ARXIV_ID = "1706.03762"
SAMPLE_RESEARCH_PROMPT = "Explain the difference between Self-Attention and Cross-Attention."
SAMPLE_FORMULA_QUERY = "Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V"
