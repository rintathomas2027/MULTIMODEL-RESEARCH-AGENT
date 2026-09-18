"""
Page Object Models for ScholarPulse AI Studio UI
"""
from .base_page import BasePage
from .workspace_page import WorkspacePage
from .auth_modal_page import AuthModalPage
from .upload_modal_page import UploadModalPage
from .external_resolver_page import ExternalResolverPage
from .command_hub_page import CommandHubPage
from .research_tabs_page import (
    ChatTabPOM,
    CitationsTabPOM,
    ScholarCastTabPOM,
    CriticalRoastTabPOM,
    FormulaCodeTabPOM,
    ExplainTabPOM,
    PresentationTabPOM,
    VivaTabPOM,
    CrossPaperMatrixModalPOM,
    AnalyticsModalPOM,
    FeedbackModalPOM
)
