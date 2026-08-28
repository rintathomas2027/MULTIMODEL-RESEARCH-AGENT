# ⚡ ScholarPulse AI Studio - Intelligent Multimodal Research & Citation Assistant

An extraordinary, enterprise-grade AI Research Intelligence Platform built with **Django REST Framework**, **Google Gemini Multi-Engine**, **ChromaDB Vector Store**, and an **Obsidian & Liquid Gold Cyber-Academic Studio Design**. Designed to surpass legacy reference managers (**Mendeley, Zotero**) and AI study tools (**SciSpace, Elicit, Google NotebookLM**).

---

## 🌟 14 Cutting-Edge Research Modules

1. **DOI / ArXiv 1-Click Paper Ingestion**: Instant paper ingestion and vector embedding via CrossRef and arXiv APIs.
2. **Mendeley & Zotero Citation Hub**: Auto-formats in APA 7th, IEEE, Harvard, MLA 9, Chicago, BibTeX, and RIS formats with 1-click Overleaf/Zotero downloads.
3. **Cross-Paper Synthesis Matrix (Elicit/SciSpace Killer)**: Select multiple papers to generate comparative literature review tables (Methodology, Dataset, Findings, Gaps) with CSV exports.
4. **"ScholarCast" Dual-Host Audio Deep Dive (NotebookLM Killer)**: Converts papers into engaging podcast dialogues with in-browser Web Speech audio synthesis, speed controls, live waveforms, and synchronized transcripts.
5. **Reviewer #2 Critical Rigor Auditor**: Ruthless peer review simulator with Rigor Score (0-100), fatal flaws detector, baseline audit, and defense directives.
6. **Multimodal Formula & Algorithm-to-Code Synthesizer**: Converts LaTeX mathematical equations into executable Python / PyTorch code with complexity bounds.
7. **Semantic RAG Copilot**: Grounded research QA and context retrieval powered by ChromaDB.
8. **Adaptive 4-Level Explain Engine**: Explains concepts tailored for Beginner, Undergraduate, MCA Engineer, or Research Scholar tiers.
9. **Automated Presentation Deck Generator**: Generates 5-slide academic presentations with detailed speaker scripts.
10. **University Viva & Defense Exam Prep**: Generates 2-Mark definitions, 5-Mark architectural questions, and challenging external examiner viva questions.
11. **Universal Command Hub (`Ctrl + K` / `Cmd + K`)**: Spotlight-style keyboard navigation and instant tool triggers.
12. **Bionic Dark / Light Theme Engine**: Seamless toggle between Obsidian Titanium Dark mode and Liquid Platinum Ivory light mode.
13. **Multi-Format Document Parsing**: High-fidelity text extraction from PDF, DOCX, PPTX, and TXT files.
14. **User Profile & Persona Customization**: Academic avatar customization and personalized study profiles.

---

## 🚀 Setup & Launch Instructions

Follow these step-by-step instructions to get your local environment running.

### Step 1: Open Terminal in Project Directory
Open your terminal (PowerShell or Command Prompt) and navigate to your project workspace:
```powershell
cd C:\AIStudyAssistant
```

### Step 2: Set Up Python Virtual Environment
Create and activate a clean virtual environment to keep dependencies insulated:
```powershell
# Create venv
python -m venv venv

# Activate venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate venv (Command Prompt)
.\venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
Install all required libraries specified in the requirements document:
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Local MySQL Database
1. Open your MySQL client (XAMPP Control Panel, phpMyAdmin, MySQL Workbench, or Command Line).
2. Create a new database named `ai_study_assistant`:
   ```sql
   CREATE DATABASE ai_study_assistant CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### Step 5: Update Your Environment Variables (`.env`)
Open the `.env` file located in the root of `C:\AIStudyAssistant\` and configure:
- **MySQL Credentials**: Add your `DB_USER` (usually `root`), `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.
- **Gemini API Key**: Retrieve an API key from Google AI Studio and set it to `GEMINI_API_KEY`.
```env
# .env Configuration File Example
SECRET_KEY=django-insecure-ai-study-assistant-super-secret-key-12345
DEBUG=True

DB_NAME=ai_study_assistant
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
```

### Step 6: Generate Database Migrations & Tables
Apply schema tables to your MySQL database:
```powershell
# Create Django migrations
python manage.py makemigrations users
python manage.py makemigrations assistant

# Run migrations
python manage.py migrate
```

### Step 7: Create a Superuser (Optional)
If you wish to access the admin portal:
```powershell
python manage.py createsuperuser
```

### Step 8: Start the Server
Run the local development server:
```powershell
python manage.py runserver
```

Open your web browser and navigate to **`http://127.0.0.1:8000/`** to experience your new **AI Study Assistant**!
