from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import StudentProfile
from .serializers import StudentProfileSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Students can only edit their own profile; consultants & admins can view others."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user', 'assigned_consultant')
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['state', 'district', 'education_level', 'assigned_consultant']
    search_fields = ['user__email', 'user__username', 'state', 'district']

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return self.queryset.filter(user=user)
        elif user.user_type == 'consultant':
            return self.queryset.filter(assigned_consultant__user=user)
        elif user.is_superuser or user.user_type == 'admin':
            return self.queryset
        return StudentProfile.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me')
    def my_profile(self, request):
        """Return the currently logged-in student's profile."""
        profile = self.get_queryset().filter(user=request.user).first()
        if not profile:
            return Response({"detail": "Profile not found"}, status=404)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
