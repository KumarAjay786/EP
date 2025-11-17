from django.db import models
from django.conf import settings
from django.utils import timezone


class StudentProfile(models.Model):
    EDUCATION_LEVELS = [
        ('10', '10th Grade'),
        ('12', '12th Grade'),
        ('ug', 'Undergraduate'),
        ('pg', 'Postgraduate'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS, blank=True, null=True)
    school_college_name = models.CharField(max_length=255, blank=True, null=True)
    percentage_or_grade = models.CharField(max_length=20, blank=True, null=True)
    passing_year = models.CharField(max_length=10, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    profile_photo = models.ImageField(upload_to='students/profile_photos/', blank=True, null=True)
    id_proof = models.FileField(upload_to='students/id_proofs/', blank=True, null=True)
    last_mark_sheet = models.FileField(upload_to='students/mark_sheets/', blank=True, null=True)

    assigned_consultant = models.ForeignKey(
        'Consultant.ConsultantProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_students'
    )

    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} ({self.user.get_user_type_display()})"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def check_profile_completion(self):
        """Automatically mark profile as complete if major fields are filled"""
        required_fields = [
            self.date_of_birth, self.address, self.state, self.district,
            self.education_level, self.last_mark_sheet
        ]
        self.profile_completed = all(required_fields)
        self.save(update_fields=['profile_completed'])
