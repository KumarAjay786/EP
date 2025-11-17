from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create a counsellor user (pre-verified)"

    def handle(self, *args, **options):
        email = input("📧 Enter counsellor email: ").strip()
        password = input("🔑 Enter password: ").strip()

        if not email or not password:
            self.stdout.write(self.style.ERROR("❌ Email and password are required."))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("❌ User already exists."))
            return

        username = email.split('@')[0]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type='counsellor',
            is_staff=True,
            email_verified=True,
            phone_verified=True,
            verified=True,
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Counsellor '{email}' created successfully!"))
