import os
import sys
import django
import traceback

# ensure project root is on PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EDUCATION_PIONEER.settings')
django.setup()

from User.serializers import RegisterSerializer
import uuid

try:
    unique = uuid.uuid4().hex[:8]
    data = {'email': f'recursion_test_{unique}@example.com', 'password': 'TestPass123!', 'password2': 'TestPass123!', 'user_type': 'student', 'phone': '9999999999'}
    s = RegisterSerializer(data=data)
    s.is_valid(raise_exception=True)
    user = s.save()
    print('User created:', user.email)
except Exception as e:
    print('Exception type:', type(e))
    traceback.print_exc()
