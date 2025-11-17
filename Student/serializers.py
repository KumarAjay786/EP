from rest_framework import serializers
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.username", read_only=True)
    age = serializers.ReadOnlyField()
    assigned_consultant_email = serializers.EmailField(
        source="assigned_consultant.user.email", read_only=True
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id", "email", "full_name", "date_of_birth", "age", "gender",
            "address", "country", "state", "district", "pincode",
            "education_level", "school_college_name", "percentage_or_grade",
            "passing_year", "interests",
            "profile_photo", "id_proof", "last_mark_sheet",
            "assigned_consultant", "assigned_consultant_email",
            "profile_completed", "created_at", "updated_at"
        ]
        read_only_fields = ["assigned_consultant", "profile_completed", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        """Auto-check profile completion on update"""
        profile = super().update(instance, validated_data)
        profile.check_profile_completion()
        return profile
