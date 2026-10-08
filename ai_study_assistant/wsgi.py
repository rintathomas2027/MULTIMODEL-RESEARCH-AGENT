import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_assistant.settings')

application = get_wsgi_application()
app = application

# If running in serverless (e.g. Vercel), populate /tmp/db.sqlite3 from the bundled database
try:
    import shutil
    from pathlib import Path
    from django.conf import settings

    if os.getenv('VERCEL', '0') == '1' or 'VERCEL_ENV' in os.environ:
        tmp_db = Path('/tmp') / 'db.sqlite3'
        bundled_db = settings.BASE_DIR / 'db.sqlite3'
        if not tmp_db.exists() and bundled_db.exists():
            try:
                shutil.copy2(bundled_db, tmp_db)
                print("Restored existing database to /tmp/db.sqlite3")
            except Exception as copy_err:
                print(f"DB restore note: {copy_err}")

    from django.core.management import call_command
    call_command('migrate', interactive=False)
    
    # Auto-seed sample research papers if database is empty
    from assistant.models import Document
    if Document.objects.count() == 0:
        try:
            import seed_demo_data
            seed_demo_data.seed()
        except Exception as seed_err:
            print(f"Auto-seed notice: {seed_err}")
except Exception as e:
    print(f"Serverless startup init notice: {e}")
