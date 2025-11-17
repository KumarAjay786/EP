from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_email',
        'state',
        'district',
        'education_level',
        'assigned_consultant',
        'profile_completed',
        'created_at',
    )
    list_filter = (
        'state',
        'district',
        'education_level',
        'profile_completed',
        'assigned_consultant__consultant_type',
    )
    search_fields = (
        'user__email',
        'user__username',
        'state',
        'district',
        'assigned_consultant__user__email',
    )
    autocomplete_fields = ('assigned_consultant',)
    readonly_fields = ('user_email',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('user_email', 'date_of_birth', 'address')
        }),
        ('Location', {
            'fields': ('country', 'state', 'district')
        }),
        ('Education', {
            'fields': ('education_level', 'interests')
        }),
        ('Consultant Assignment', {
            'fields': ('assigned_consultant', 'profile_completed')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'user_email')

    def user_email(self, obj):
        return obj.user.email if obj.user else "-"
    user_email.short_description = "Student Email"

    ordering = ('-created_at',)
