import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cabapp.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin_test').exists():
    User.objects.create_superuser('admin_test', 'admin@example.com', 'AdminPass123!')
    print("Superuser created.")
else:
    print("Superuser exists.")
