from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
import random
import uuid
from django.contrib.auth.hashers import make_password



# -----------------------------
# Custom User Manager
# -----------------------------
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with an email."""
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email.split('@')[0])
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "admin")
        extra_fields.setdefault("verified", True)
        extra_fields.setdefault("email_verified", True)
        extra_fields.setdefault("phone_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# -----------------------------
# User Model
# -----------------------------
class User(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('consultant', 'Consultant'),
        ('college', 'College'),
        ('counsellor', 'Counsellor'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=255, help_text="Full name of student/consultant or institution name", null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)

    # Verification fields
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)  # true if both verified
    is_profile_complete = models.BooleanField(default=False, help_text="True if profile setup is complete")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.user_type})"

    def update_verification_status(self):
        """Set verified=True only when both email and phone are verified."""
        if self.email_verified and self.phone_verified:
            # mark as verified and activate the account when both verifications are done
            self.verified = True
            # only set is_active True once both verifications are complete
            if not self.is_active:
                self.is_active = True
                self.save(update_fields=['verified', 'is_active'])
            else:
                self.save(update_fields=['verified'])

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['name', 'email']


# -----------------------------
# Email OTP Verification
# -----------------------------
class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def generate_otp(self):
        """Generate and save a 6-digit OTP for email."""
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def is_valid(self):
        """Check if the OTP is still valid (10 min)."""
        return (timezone.now() - self.created_at).seconds < 600  # 10 minutes validity

    def __str__(self):
        return f"Email OTP for {self.user.email}"


# -----------------------------
# Phone OTP Verification
# -----------------------------
class PhoneOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def generate_otp(self):
        """Generate and save a 6-digit OTP for phone."""
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def is_valid(self):
        """Check if the OTP is still valid (10 min)."""
        return (timezone.now() - self.created_at).seconds < 600

    def __str__(self):
        return f"Phone OTP for {self.user.phone}"


# -----------------------------
# Pre-registration (pending) model
# -----------------------------
class PreRegistration(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    password_hash = models.CharField(max_length=128)
    user_type = models.CharField(max_length=20, choices=User.USER_TYPES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)
        self.save(update_fields=['password_hash'])

    def is_fully_verified(self):
        return self.email_verified and self.phone_verified

    def __str__(self):
        return f"PreRegistration {self.email} ({self.token})"


class PreEmailOTP(models.Model):
    pre = models.ForeignKey(PreRegistration, on_delete=models.CASCADE, related_name='email_otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 600


class PrePhoneOTP(models.Model):
    pre = models.ForeignKey(PreRegistration, on_delete=models.CASCADE, related_name='phone_otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 600



