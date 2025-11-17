from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ConsultantProfile


@receiver(pre_save, sender=ConsultantProfile)
def assign_parent_consultant(sender, instance, **kwargs):
    """
    Automatically link district consultants to their parent state consultant.
    Also prevents multiple state consultants for the same state.
    """
    # Prevent multiple state consultants for same state
    if instance.consultant_type == 'state':
        existing = ConsultantProfile.objects.filter(
            state=instance.state, consultant_type='state'
        ).exclude(pk=instance.pk)
        if existing.exists():
            raise ValueError(f"A state consultant already exists for {instance.state}.")

    # Auto-link district consultant to its parent state consultant
    if instance.consultant_type == 'district' and not instance.parent_consultant:
        state_consultant = ConsultantProfile.objects.filter(
            state=instance.state, consultant_type='state', verified=True
        ).first()
        instance.parent_consultant = state_consultant


@receiver(post_save, sender=ConsultantProfile)
def send_consultant_notifications(sender, instance, created, **kwargs):
    """
    Send email notifications to:
    - Admin/Counsellor when a new consultant registers.
    - Consultant when approved/verified.
    """

    # ✅ When a consultant is newly created (registered)
    if created:
        subject = f"New Consultant Registration - {instance.full_name}"
        message = (
            f"A new consultant has registered for {instance.state} / {instance.district or 'N/A'}.\n"
            f"Consultant Name: {instance.full_name}\n"
            f"Email: {instance.user.email}\n"
            f"Type: {instance.consultant_type}\n\n"
            f"Please review and approve in the admin dashboard."
        )
        # Notify counsellors/admins
        from User.models import User
        recipients = list(
            User.objects.filter(user_type__in=['admin', 'counsellor']).values_list('email', flat=True)
        )
        if recipients:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)

    # ✅ When a consultant is verified/approved
    else:
        # Send notification only when verified status changes to True
        if instance.verified and instance.approved_by:
            subject = "Your Consultant Account Has Been Approved ✅"
            message = (
                f"Dear {instance.full_name},\n\n"
                f"Your consultant account for {instance.state} / {instance.district or 'N/A'} "
                f"has been approved by {instance.approved_by.email}.\n\n"
                "You can now access your consultant dashboard and start managing student applications."
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=True)
