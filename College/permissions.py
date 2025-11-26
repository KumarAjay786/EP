from rest_framework import permissions
from .models import CollegeProfile


class IsCollegeOwner(permissions.BasePermission):
    """
    Permission to check if user is the owner of the college.
    Used to restrict access to college-specific resources.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check if user is the college owner"""
        # Allow safe methods for college owners viewing their own data
        if request.method in permissions.SAFE_METHODS:
            # For direct college profile access
            if hasattr(obj, 'user'):
                return obj.user == request.user
            # For resources (courses, faculty, events, etc.) that have college FK
            if hasattr(obj, 'college'):
                return obj.college.user == request.user
        
        # For write operations, user must be the college owner
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'user'):
                return obj.user == request.user
            if hasattr(obj, 'college'):
                return obj.college.user == request.user
        
        return False


class IsCollegeOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to allow college owners to manage their resources,
    but allow read-only access to other authenticated users.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write operations, only college owner can modify
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'college'):
            return obj.college.user == request.user
        
        return False


class IsCollegeAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to restrict write access to college admins only,
    but allow read access to authenticated users.
    
    Used for resources like courses, faculty, events that should be
    visible to others but editable only by college owner.
    """
    
    def has_permission(self, request, view):
        # Allow GET requests for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # For write operations, user must be authenticated and have college profile
        if request.user and request.user.is_authenticated:
            try:
                college = request.user.college_profile
                return college is not None
            except CollegeProfile.DoesNotExist:
                return False
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Allow read access to all
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write operations, check college ownership
        if hasattr(obj, 'college'):
            return obj.college.user == request.user
        
        return False
