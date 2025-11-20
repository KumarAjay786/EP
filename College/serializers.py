from rest_framework import serializers
from .models import CollegeProfile,Course,Event,Gallery,Faculty,Hostel


class CollegeProfileSerializer(serializers.ModelSerializer):
    """Serializer for CollegeProfile model."""

    # Read-only system-generated fields
    college_code = serializers.CharField(read_only=True)
    verified = serializers.BooleanField(read_only=True)
    approved_by = serializers.StringRelatedField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)
    
    # Dynamically get main streams from related courses
    main_streams = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CollegeProfile
        fields = [
            # --- Basic Info ---
            "id",
            "college_name",
            "college_code",
            "official_registration_no",
            "college_type",
            "established_year",
            "accreditation_body",

            # --- Contact & Location ---
            "country",
            "state",
            "district",
            "pin_code",
            "address",
            "email",
            "phone",
            "website",

            # --- Dashboard Editable ---
            "about_college",
            "college_logo",
            "college_image",
            "credential_image",
            "landline",
            "contact_person",

            # --- System / Meta ---
            "verified",
            "approved_by",
            "approved_at",
            "is_popular",
            "is_featured",
            "main_streams",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "college_code",
            "verified",
            "approved_by",
            "approved_at",
            "is_popular",
            "is_featured",
            "main_streams",
            "created_at",
            "updated_at",
        ]
    
    def get_main_streams(self, obj):
        """Get unique main streams from related courses"""
        main_streams = obj.courses.values_list('main_stream', flat=True).distinct()
        return list(main_streams)

    def create(self, validated_data):
        """Create college profile and mark profile complete if valid."""
        college_profile = CollegeProfile.objects.create(**validated_data)
        college_profile.mark_profile_complete()
        return college_profile

    def update(self, instance, validated_data):
        """Update college profile and mark user profile complete."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.mark_profile_complete()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    college_code = serializers.CharField(source='college.college_code', read_only=True)
    college_name = serializers.CharField(source='college.college_name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'college',
            'college_code',
            'college_name',
            'main_stream',
            'degree',
            'level',
            'specialization',
            'duration',
            'fee',
            'eligibility',
            'description',
            'brochure',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_brochure_url(self, obj):
        """Return full URL for brochure file"""
        request = self.context.get('request')
        if obj.brochure and request:
            return request.build_absolute_uri(obj.brochure.url)
        return None     



class EventSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'college', 'college_name', 'name', 'date',
            'location', 'description', 'image', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class GallerySerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    college_name = serializers.CharField(source="college.college_name", read_only=True)  # optional

    class Meta:
        model = Gallery
        fields = [
            "id",
            "college",
            "college_name",
            "media_type",
            "file",
            "file_url",
            "title",
            "description",
            "display_order",
            "created_at",
        ]
        read_only_fields = ["id", "file_url", "created_at", "college_name", "college"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and hasattr(obj.file, "url"):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            "id",
            "college",
            "name",
            "designation",
            "qualification",
            "experience",
            "department",
            "email",
            "photo",
            "is_active",
            "display_order",
            "created_at",
        ]
        read_only_fields = ["college","id", "created_at"]

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = "__all__"

