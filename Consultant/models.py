from django.db import models
from django.conf import settings

class ConsultantProfile(models.Model):
    CONSULTANT_TYPES = [
        ('pending', 'Pending Approval'),
        ('state', 'State Consultant'),
        ('district', 'District Consultant'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultant_profile'
    )
    consultant_type = models.CharField(max_length=20, choices=CONSULTANT_TYPES, default='pending')
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    parent_consultant = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_consultants'
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='consultants/profile/', blank=True, null=True)
    
    id_proof = models.FileField(upload_to='consultants/id_proofs/', blank=True, null=True)
    qualification_certificate = models.FileField(upload_to='consultants/certificates/', blank=True, null=True)
    experience_certificate = models.FileField(upload_to='consultants/experience/', blank=True, null=True)

    verified = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_consultants'
    )
    approved_at = models.DateTimeField(blank=True, null=True)

    total_students = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_consultant_type_display()} ({self.state}, {self.district or 'N/A'})"

    def save(self, *args, **kwargs):
        if self.consultant_type == 'state':
            existing = ConsultantProfile.objects.filter(
                state=self.state,
                consultant_type='state'
            ).exclude(pk=self.pk)
            if existing.exists():
                raise ValueError(f"A state consultant already exists for {self.state}.")
        super().save(*args, **kwargs)
