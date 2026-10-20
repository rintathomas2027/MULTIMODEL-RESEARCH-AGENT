import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_assistant.settings')

def export_data():
    try:
        django.setup()
        from django.core.management import call_command
        
        output_file = BASE_DIR / 'data_dump.json'
        print(f"[*] Exporting database records to {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--exclude', 'contenttypes',
                '--exclude', 'auth.permission',
                '--indent', '2',
                stdout=f
            )
        
        size = os.path.getsize(output_file)
        print(f"[+] Successfully exported {size} bytes to data_dump.json!")
    except Exception as e:
        print(f"[-] Export warning/error: {e}")

if __name__ == '__main__':
    export_data()
