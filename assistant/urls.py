from django.urls import path
from .views import (
    DocumentListCreateView,
    DocumentDetailDeleteView,
    RAGChatView,
    SummarizeDocumentView,
    ExplainModeView,
    PresentationAssistantView,
    VivaGeneratorView,
    CitationGeneratorView,
    CrossPaperMatrixView,
    ScholarCastView,
    CriticalRoastView,
    FormulaCodeView,
    ExternalPaperResolverView
)

urlpatterns = [
    # Document Workspace (Module 2 & 3)
    path('workspace/documents/', DocumentListCreateView.as_view(), name='doc_list_create'),
    path('workspace/documents/<int:pk>/', DocumentDetailDeleteView.as_view(), name='doc_detail_delete'),

    # DOI / ArXiv 1-Click External Paper Ingestion (Module 14)
    path('workspace/documents/resolve-external/', ExternalPaperResolverView.as_view(), name='resolve_external_paper'),

    # Cross-Paper Comparative Synthesis Matrix (Module 10)
    path('workspace/documents/cross-matrix/', CrossPaperMatrixView.as_view(), name='cross_paper_matrix'),

    # AI Research Assistant & Summarizer (Module 5)
    path('workspace/documents/<int:pk>/chat/', RAGChatView.as_view(), name='rag_chat'),
    path('workspace/documents/<int:pk>/summarize/', SummarizeDocumentView.as_view(), name='summarize_doc'),

    # Academic Citation & Reference Intelligence (Module 9 - Mendeley/Zotero Killer)
    path('workspace/documents/<int:pk>/citations/', CitationGeneratorView.as_view(), name='doc_citations'),

    # "ScholarCast" Dual-Host Audio Deep Dive (Module 11 - NotebookLM Killer)
    path('workspace/documents/<int:pk>/podcast/', ScholarCastView.as_view(), name='scholarcast_podcast'),

    # "Reviewer #2" Critical Roast & Rigor Auditor (Module 12)
    path('workspace/documents/<int:pk>/roast/', CriticalRoastView.as_view(), name='critical_roast'),

    # Multimodal Math Formula to Code Synthesizer (Module 13)
    path('workspace/documents/<int:pk>/formula-code/', FormulaCodeView.as_view(), name='formula_code'),

    # AI Explain Mode (Module 6)
    path('workspace/documents/<int:pk>/explain/', ExplainModeView.as_view(), name='explain_mode'),

    # AI Presentation Assistant (Module 7)
    path('workspace/documents/<int:pk>/presentation/', PresentationAssistantView.as_view(), name='presentation_assistant'),

    # AI Viva Generator (Module 8)
    path('workspace/documents/<int:pk>/viva/', VivaGeneratorView.as_view(), name='viva_generator'),
]
