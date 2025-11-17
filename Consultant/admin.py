from django.contrib import admin
from .models import ConsultantProfile


@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(admin.ModelAdmin):
	"""Admin for ConsultantProfile.

	Provides search support so other ModelAdmins can use this model in
	`autocomplete_fields` (StudentProfile.assigned_consultant, etc.).
	"""
	list_display = ('full_name', 'user', 'consultant_type', 'state', 'district', 'verified')
	search_fields = ('full_name', 'user__email', 'user__username')
	list_filter = ('consultant_type', 'state', 'district', 'verified')
	readonly_fields = ('created_at',)
