from rest_framework import serializers
from .models import ConsultantProfile
from User.models import User  # assuming user app is named 'users'


class ConsultantProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_type = serializers.CharField(source='user.user_type', read_only=True)

    class Meta:
        model = ConsultantProfile
        fields = [
            'id', 'user_email', 'user_type', 'consultant_type', 'state', 'district',
            'full_name', 'phone', 'address', 'profile_image',
            'id_proof', 'qualification_certificate', 'experience_certificate',
            'verified', 'approved_by', 'approved_at', 'total_students', 'rating', 'created_at'
        ]
        read_only_fields = ['approved_by', 'approved_at', 'verified', 'rating', 'total_students']


class ConsultantCreateSerializer(serializers.ModelSerializer):
    """For consultants registering themselves"""
    class Meta:
        model = ConsultantProfile
        fields = ['state', 'district', 'full_name', 'phone', 'address', 'profile_image',
                  'id_proof', 'qualification_certificate', 'experience_certificate']

    def create(self, validated_data):
        user = self.context['request'].user
        consultant = ConsultantProfile.objects.create(user=user, **validated_data)
        return consultant


class ConsultantApprovalSerializer(serializers.ModelSerializer):
    """Used by counsellor/admin to approve consultant"""
    class Meta:
        model = ConsultantProfile
        fields = ['verified', 'consultant_type']

    def update(self, instance, validated_data):
        request = self.context['request']
        instance.verified = validated_data.get('verified', instance.verified)
        instance.consultant_type = validated_data.get('consultant_type', instance.consultant_type)
        instance.approved_by = request.user
        from django.utils import timezone
        instance.approved_at = timezone.now()
        instance.save()
        return instance
