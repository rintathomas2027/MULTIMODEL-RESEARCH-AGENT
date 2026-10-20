# Render Backend Deployment Guide (Zero Data Loss)

This guide walks you through deploying the **ScholarPulse AI Backend** to [Render](https://render.com) while preserving **100% of your data** (all existing user accounts, documents, notes, quizzes, and AI vector embeddings).

---

## Step 1: Export Data and Push to GitHub

We have configured `push_to_git.bat` to automatically back up your entire SQLite database into a portable fixture (`data_dump.json`) before pushing.

1. In your project folder `C:\AIStudyAssistant`, double-click:
   ```cmd
   push_to_git.bat
   ```
2. The script will:
   - Export all users, documents, summaries, and chat histories into `data_dump.json`.
   - Stage and track `db.sqlite3`, `data_dump.json`, `media/documents/` (all 16 uploaded papers), and `chroma_db/`.
   - Commit and push everything to your GitHub repository:
     `https://github.com/rintathomas2027/MULTIMODEL-RESEARCH-AGENT`

---

## Step 2: Deploy on Render

### Method A: Blueprint Deploy (Recommended - Fast & Automated)
1. Log in to [dashboard.render.com](https://dashboard.render.com/).
2. Click **New +** in the top navigation bar and select **Blueprint**.
3. Connect your GitHub account and select your repository:
   `rintathomas2027/MULTIMODEL-RESEARCH-AGENT`
4. Render will automatically read `render.yaml`:
   - It preconfigures the build command (`./build.sh`), start command (`gunicorn ai_study_assistant.wsgi:application`), and runtime.
5. In the Environment Variables section, enter your:
   - **`GEMINI_API_KEY`**: Your Google Gemini API key.
6. Click **Apply**. Render will build and deploy your service!

---

### Method B: Manual Web Service Setup
If you prefer configuring the Web Service manually:
1. Go to [dashboard.render.com](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Select your repository: `rintathomas2027/MULTIMODEL-RESEARCH-AGENT` and branch: `main`.
4. Fill in the following settings:
   - **Name**: `scholarpulse-backend`
   - **Region**: Oregon (US West) or Ohio (US East)
   - **Branch**: `main`
   - **Root Directory**: *(Leave blank)*
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     ./build.sh
     ```
   - **Start Command**:
     ```bash
     gunicorn ai_study_assistant.wsgi:application
     ```
   - **Plan**: `Free`
5. Click **Advanced** and add the following **Environment Variables**:
   | Key | Value | Description |
   |---|---|---|
   | `PYTHON_VERSION` | `3.11.9` | Matches your development environment |
   | `GEMINI_API_KEY` | `your_actual_gemini_key` | Powers the 14 AI research modules |
   | `SECRET_KEY` | `django-insecure-render-super-secret-key-123` *(or click Generate)* | Django secret key |
   | `DEBUG` | `False` | Production mode |
   | `DB_ENGINE` | `sqlite` | Uses bundled database |
6. Click **Create Web Service**.

---

## Step 3: Verify Your Deployment & Data

1. Once the deployment status turns green (**Live**), Render will provide your public URL:
   ```
   https://scholarpulse-backend.onrender.com
   ```
2. Test the health and data endpoints:
   - **Frontend UI / Home**: `https://scholarpulse-backend.onrender.com/`
   - **Admin Portal**: `https://scholarpulse-backend.onrender.com/admin/`
   - **Document List API**: `https://scholarpulse-backend.onrender.com/api/documents/`
   - **Test Document Download**: `https://scholarpulse-backend.onrender.com/media/documents/Prompt_Engineering_Fundamentals.pdf`

All 16 research documents and your user accounts (e.g. `MCA_Evaluator`) will be ready and accessible!

---

## Understanding Data Persistence on Render

### Current Setup (Zero Data Loss)
- Your entire current state (`db.sqlite3`, `data_dump.json`, all 16 PDFs in `media/documents`, and vector embeddings in `chroma_db`) is packaged directly with your repository.
- Every time you run `push_to_git.bat` locally, your local changes are saved into `data_dump.json` and redeployed to Render.

### If you want permanent cloud persistence for new uploads made directly on Render:
- Render's **Free Tier Web Service** uses ephemeral disks (meaning files created during runtime reset when the free container sleeps or redeploys).
- If you want new user registrations or new uploads made on the live web app to permanently persist across restarts:
  1. **Option A (Free Cloud Postgres)**: Create a free PostgreSQL database on Render (click **New +** -> **PostgreSQL**). Copy the **Internal Database URL** and add it as `DATABASE_URL` in your Web Service environment variables. Our backend will automatically detect `DATABASE_URL`, connect to Postgres, and import your `data_dump.json` automatically!
  2. **Option B (Render Persistent Disk)**: On a paid Render instance ($7/mo Starter), you can attach a persistent disk mounted to `/var/data` for permanent file and SQLite storage.
