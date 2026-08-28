import os
import PyPDF2
from docx import Document as DocxDocument
from pptx import Presentation

def extract_text_from_file(file_path, file_type):
    """
    Extract text content from uploaded file based on extension (.pdf, .docx, .pptx, .txt).
    Returns clean string text.
    """
    file_type = file_type.lower().replace('.', '')
    text = ""

    try:
        if file_type == 'pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages_text = []
                for i, page in enumerate(reader.pages):
                    page_content = page.extract_text() or ""
                    if page_content.strip():
                        pages_text.append(f"[Page {i+1}]\n{page_content.strip()}")
                text = "\n\n".join(pages_text)

        elif file_type in ['docx', 'doc']:
            doc = DocxDocument(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n".join(paragraphs)

        elif file_type in ['pptx', 'ppt']:
            prs = Presentation(file_path)
            slides_text = []
            for i, slide in enumerate(prs.slides):
                slide_content = []
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text:
                        slide_content.append(shape.text.strip())
                if slide_content:
                    slides_text.append(f"[Slide {i+1}]\n" + "\n".join(slide_content))
            text = "\n\n".join(slides_text)

        elif file_type in ['txt', 'md']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

        elif file_type in ['png', 'jpg', 'jpeg', 'webp', 'bmp']:
            # Multimodal Vision Extraction via PIL & Gemini Vision
            text = extract_multimodal_image_insights(file_path)

        else:
            text = f"Unsupported file type: {file_type}"

    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        text = f"Error processing file: {str(e)}"

    return clean_text(text)

def clean_text(text):
    if not text:
        return ""
    # Basic text normalization
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def extract_multimodal_image_insights(image_path):
    """
    Extracts deep visual semantic context, OCR text, data charts, and architecture diagrams using Gemini Vision.
    """
    try:
        from PIL import Image
        import google.generativeai as genai
        import os

        img = Image.open(image_path)
        api_key = os.getenv('GEMINI_API_KEY', '').strip()

        if api_key:
            genai.configure(api_key=api_key)
            prompt = """
You are ScholarPulse AI's Multimodal Visual Perception Engine.
Analyze this academic image / diagram / flowchart / architecture chart / research figure in detail.

Provide a comprehensive extraction in the following format:
[VISUAL ENTITY & DIAGRAM TYPE]
- Identify if this is a System Architecture, Flowchart, Scatter Plot, Bar Chart, Mathematical Formula, or UI Mockup.

[TRANSCRIPTION & LABELS]
- Transcribe all text, numbers, formulas, and labels present in the image.

[SYSTEM ARCHITECTURE & DATA FLOW BREAKDOWN]
- Detail each component, input streams, processing layers, and output outcomes.

[RESEARCH IMPLICATIONS & CORE TAKEAWAYS]
- Explain what this figure contributes to the research project or technical study.
"""
            model_names = ['gemini-2.0-flash', 'gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro-vision']
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    res = model.generate_content([prompt, img])
                    if res and res.text:
                        return f"[Multimodal Visual Analysis: {os.path.basename(image_path)}]\n\n" + res.text
                except Exception:
                    continue

        # Fallback if no API key or vision call fails
        width, height = img.size
        format_name = img.format or 'IMAGE'
        return f"[Image Document: {os.path.basename(image_path)}]\nResolution: {width}x{height}px\nFormat: {format_name}\nContains visual research diagram / architectural layout."

    except Exception as e:
        print(f"Error in extract_multimodal_image_insights: {e}")
        return f"[Image Document: {os.path.basename(image_path)}]\nError analyzing visual contents: {str(e)}"

