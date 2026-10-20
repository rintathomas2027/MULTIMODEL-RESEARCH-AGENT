import os
import sys
import shutil
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_assistant.settings')

# Restore SQLite database to /tmp/db.sqlite3 if in serverless environment
if os.getenv('VERCEL', '0') == '1' or 'VERCEL_ENV' in os.environ or 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
    tmp_db = Path('/tmp') / 'db.sqlite3'
    bundled_db = BASE_DIR / 'db.sqlite3'
    if not tmp_db.exists() and bundled_db.exists():
        try:
            shutil.copy2(bundled_db, tmp_db)
            print("Restored database to /tmp/db.sqlite3")
        except Exception as copy_err:
            print(f"DB restore note: {copy_err}")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application

# Run migrations safely and restore data if database is fresh
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    
    from assistant.models import Document
    if Document.objects.count() == 0:
        data_dump_file = BASE_DIR / 'data_dump.json'
        if data_dump_file.exists():
            try:
                call_command('loaddata', str(data_dump_file))
                print("Restored existing database from data_dump.json successfully")
            except Exception as load_err:
                print(f"loaddata note: {load_err}")

        # If still 0 (e.g. data_dump was not present), seed default demo papers
        if Document.objects.count() == 0:
            try:
                import seed_demo_data
                seed_demo_data.seed()
            except Exception as seed_err:
                print(f"Auto-seed note: {seed_err}")
except Exception as e:
    print(f"Startup init note: {e}")
