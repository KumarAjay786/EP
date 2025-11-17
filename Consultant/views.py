from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import ConsultantProfile
from .serializers import (
    ConsultantProfileSerializer,
    ConsultantCreateSerializer,
    ConsultantApprovalSerializer
)
from User.models import User


class IsCounsellorOrAdmin(permissions.BasePermission):
    """Only counsellor or admin can approve"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['counsellor', 'admin']


class ConsultantListView(generics.ListAPIView):
    queryset = ConsultantProfile.objects.all().order_by('-created_at')
    serializer_class = ConsultantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['consultant_type', 'verified', 'state', 'district']
    search_fields = ['full_name', 'state', 'district']

    # Optional: restrict to counsellor/admin full view
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['counsellor', 'admin']:
            return ConsultantProfile.objects.all()
        # Normal consultant sees only self
        return ConsultantProfile.objects.filter(user=user)


class ConsultantCreateView(generics.CreateAPIView):
    serializer_class = ConsultantCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.user_type != 'consultant':
            raise PermissionDenied("Only consultant users can create their profile.")
        serializer.save(user=self.request.user)


class ConsultantDetailView(generics.RetrieveUpdateAPIView):
    queryset = ConsultantProfile.objects.all()
    serializer_class = ConsultantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsultantApprovalView(generics.UpdateAPIView):
    queryset = ConsultantProfile.objects.all()
    serializer_class = ConsultantApprovalSerializer
    permission_classes = [permissions.IsAuthenticated, IsCounsellorOrAdmin]
