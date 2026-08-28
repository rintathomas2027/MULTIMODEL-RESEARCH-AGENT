from django.apps import AppConfig


class AssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assistant'

    def ready(self):
        import sys
        # Run migrations automatically on server startup
        if any(cmd in sys.argv for cmd in ['runserver', 'wsgi', 'asgi']):
            try:
                from django.core.management import call_command
                call_command('migrate', interactive=False)
                print("⚡ ScholarPulse AI: Automatic database migrations applied successfully.")
            except Exception as e:
                print(f"⚠️ ScholarPulse AI: Automatic database migration failed: {e}")
