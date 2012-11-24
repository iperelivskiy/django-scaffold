
import os
import sys
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
sys.stdout = sys.stderr  # Prevent errors with 'print' commands
application = get_wsgi_application()
