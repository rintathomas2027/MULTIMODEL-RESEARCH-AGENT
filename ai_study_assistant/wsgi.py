import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_assistant.settings')

application = get_wsgi_application()
app = application

# Run auto-migrations on serverless startup so SQLite tables exist
try:
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
