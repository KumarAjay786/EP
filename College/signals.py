from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CollegeProfile, AdmissionApplication, ConsultantProfile


# -------------------------------------------------------------------
# 🔹 1. Notify Admin when a new college registers
# -------------------------------------------------------------------
@receiver(post_save, sender=CollegeProfile)
def notify_admin_on_new_college(sender, instance, created, **kwargs):
    """Send email notification to admin when a new college registers."""
    if created and not instance.verified:
        subject = "🆕 New College Registration Pending Approval"
        message = (
            f"College '{instance.college_name}' has just registered and awaits approval.\n\n"
            f"State: {instance.state}\n"
            f"District: {instance.district}\n"
            f"Email: {instance.email or 'N/A'}\n\n"
            f"Please review and verify it in the admin panel."
        )
        admin_email = getattr(settings, "ADMIN_EMAIL", None)
        if admin_email:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])


# -------------------------------------------------------------------
# 🔹 2. Notify student when their application status changes
# -------------------------------------------------------------------
@receiver(pre_save, sender=AdmissionApplication)
def handle_application_status_change(sender, instance, **kwargs):
    """Notify student when their admission application is accepted or rejected."""
    if instance.pk:
        previous = AdmissionApplication.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            subject = None
            message = None

            if instance.status == 'accepted':
                subject = f"🎉 Application Accepted - {instance.course.name}"
                message = (
                    f"Dear {instance.student.get_full_name() or 'Student'},\n\n"
                    f"Congratulations! Your application for the course "
                    f"'{instance.course.name}' at '{instance.course.college.college_name}' "
                    f"has been accepted.\n\n"
                    f"Please proceed to complete your admission process."
                )
            elif instance.status == 'rejected':
                subject = f"❌ Application Rejected - {instance.course.name}"
                message = (
                    f"Dear {instance.student.get_full_name() or 'Student'},\n\n"
                    f"We regret to inform you that your application for "
                    f"'{instance.course.name}' at '{instance.course.college.college_name}' "
                    f"has been rejected.\n\n"
                    f"You may apply for other available courses on our platform."
                )

            if subject and message:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.student.email])


# -------------------------------------------------------------------
# 🔹 3. Automatically assign parent consultant (if applicable)
# -------------------------------------------------------------------
@receiver(pre_save, sender=ConsultantProfile)
def assign_parent_consultant(sender, instance, **kwargs):
    """Auto-assign parent consultant for district-level consultants."""
    if instance.consultant_type == 'district' and not instance.parent_consultant:
        state_consultant = ConsultantProfile.objects.filter(
            state=instance.state,
            consultant_type='state',
            verified=True
        ).first()
        if state_consultant:
            instance.parent_consultant = state_consultant
