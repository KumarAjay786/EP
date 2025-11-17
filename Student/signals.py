from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import StudentProfile
from Consultant.models import ConsultantProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'student':
        StudentProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=StudentProfile)
def update_profile_completion(sender, instance, **kwargs):
    """Safely compute and persist `profile_completed` without re-triggering post_save.

    Calling instance.save() inside this handler causes a post_save loop. Use an
    update() query to persist the boolean without emitting signals.
    """
    required_fields = [
        instance.date_of_birth,
        instance.address,
        instance.state,
        instance.district,
        instance.education_level,
        instance.last_mark_sheet,
    ]
    completed = all(required_fields)

    # Only update DB when there's an actual change to avoid unnecessary writes
    if instance.profile_completed != completed:
        StudentProfile.objects.filter(pk=instance.pk).update(profile_completed=completed)



@receiver(pre_save, sender=StudentProfile)
def assign_consultant_based_on_region(sender, instance, **kwargs):
    """Automatically assign consultant based on student's district/state."""
    if not instance.assigned_consultant and instance.state and instance.district:
        # Try district consultant first
        district_consultant = ConsultantProfile.objects.filter(
            state=instance.state,
            district=instance.district,
            consultant_type='district',
            verified=True
        ).first()

        if district_consultant:
            instance.assigned_consultant = district_consultant
        else:
            # Fallback to state consultant
            state_consultant = ConsultantProfile.objects.filter(
                state=instance.state,
                consultant_type='state',
                verified=True
            ).first()
            if state_consultant:
                instance.assigned_consultant = state_consultant
