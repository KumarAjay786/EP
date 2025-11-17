from rest_framework import permissions

class IsAdminOrCounsellor(permissions.BasePermission):
    """
    Allows access only to admin or counsellor users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'counsellor']


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow users to view/update their own profile only.
    Admins/Counsellors can view all.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.user_type in ['admin', 'counsellor']:
            return True
        return obj == request.user
