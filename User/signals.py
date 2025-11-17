from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .models import User, EmailOTP, PhoneOTP
from Student.models import StudentProfile
from Consultant.models import ConsultantProfile
from College.models import CollegeProfile


def generate_unique_code(prefix):
    """Generate a short unique code with prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


@receiver(post_save, sender=User)
def create_user_profile_and_verification(sender, instance, created, **kwargs):
    """
    Create related profile and trigger email/phone OTPs when a new User is created.
    """
    if not created:
        return

    # 1️⃣ Create related profile based on user type
    if instance.user_type == 'student':
        StudentProfile.objects.get_or_create(
            user=instance,
            defaults={'student_code': generate_unique_code('STU')}
        )

    elif instance.user_type == 'consultant':
        ConsultantProfile.objects.get_or_create(
            user=instance,
            defaults={'consultant_code': generate_unique_code('CON')}
        )

    elif instance.user_type == 'college':
        # Generate unique college code
        college_code = generate_unique_code('COL')
        while CollegeProfile.objects.filter(college_code=college_code).exists():
            college_code = generate_unique_code('COL')

        base_name = instance.name or instance.username or f"College_{instance.pk}"

        CollegeProfile.objects.get_or_create(
            user=instance,
            defaults={
                'college_name': base_name,
                'college_code': college_code,
            }
        )

    # 2️⃣ Trigger OTP verification for registerable user types
    if instance.user_type in ['student', 'consultant', 'college']:
        # ---- Email OTP ----
        email_otp_obj = EmailOTP.objects.create(user=instance)
        email_otp = email_otp_obj.generate_otp()

        subject = "Email Verification OTP"
        message = f"Hi {instance.email},\n\nYour email verification OTP is: {email_otp}\n\nThis OTP is valid for 10 minutes."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email], fail_silently=True)
        print(f"📧 Email OTP sent to {instance.email}: {email_otp}")  # Debug only

        # ---- Phone OTP ----
        if instance.phone:
            phone_otp_obj = PhoneOTP.objects.create(user=instance)
            phone_otp = phone_otp_obj.generate_otp()
            # Replace with actual SMS service later (Twilio, MSG91, etc.)
            print(f"📱 Phone OTP for {instance.phone}: {phone_otp}")  # Debug only
