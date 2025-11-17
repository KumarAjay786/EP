from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create a verified super admin user with email login"

    def handle(self, *args, **options):
        email = input("📧 Enter admin email: ").strip()
        password = input("🔑 Enter password: ").strip()

        if not email or not password:
            self.stdout.write(self.style.ERROR("❌ Email and password cannot be empty."))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("❌ A user with this email already exists."))
            return

        user = User.objects.create_superuser(
            email=email,
            password=password,
            user_type="admin",
            is_staff=True,
            is_superuser=True,
            verified=True,
            email_verified=True,
            phone_verified=True,
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Super admin '{email}' created successfully!"))
