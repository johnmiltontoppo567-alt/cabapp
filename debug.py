import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cabapp.settings')
django.setup()

try:
    from django.contrib.auth.models import User
    User.objects.filter(username='admin_test').exists()
    print("It worked")
except Exception as e:
    traceback.print_exc()
