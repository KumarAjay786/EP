# from django.contrib import admin
# from django.utils.html import format_html
# from django.urls import reverse
# from .models import CollegeProfile, Course, CollegeGallery, AdmissionApplication, CourseCategory


# # ---------- Inline for Gallery ----------
# class CollegeGalleryInline(admin.TabularInline):
#     model = CollegeGallery
#     extra = 1
#     max_num = 12
#     readonly_fields = ['uploaded_at']


# # ---------- Inline for Courses ----------
# class CourseInline(admin.TabularInline):
#     model = Course
#     extra = 1
#     fields = (
#         'name', 'category', 'duration', 'affiliation_details', 'eligibility',
#         'fees_structure', 'consultancy_incentive', 'total_seats',
#         'admission_completed', 'is_active', 'is_popular'
#     )
#     readonly_fields = ('available_seats',)


# # ---------- College Profile ----------
# @admin.register(CollegeProfile)
# class CollegeProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'college_name', 'college_code', 'state', 'district',
#         'verified_badge', 'category_list', 'course_count',
#         'total_seats', 'available_seats', 'view_site'
#     )
#     # 'categories' is the ManyToManyField on CollegeProfile (was incorrectly referenced as 'college_category')
#     list_filter = ('verified', 'state', 'district', 'categories')
#     search_fields = ('college_name', 'college_code', 'state', 'district')
#     readonly_fields = ('college_code', 'verified')
#     inlines = [CourseInline, CollegeGalleryInline]
#     actions = ['approve_college']

#     fieldsets = (
#         ('Basic Info', {
#             'fields': (
#                 'user', 'college_name', 'college_code', 'registration_number',
#                 'address', 'country', 'state', 'district', 'college_category'
#             )
#         }),
#         ('Contact', {
#             'fields': ('website', 'email', 'phone', 'landline', 'contact_person')
#         }),
#         ('Visuals & Branding', {
#             'fields': ('college_logo', 'college_image', 'credential_image', 'about_college')
#         }),
#         ('Verification', {'fields': ('verified',)})
#     )

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('courses')

#     def verified_badge(self, obj):
#         if obj.verified:
#             return format_html('<span style="color:green;">✔️ Verified</span>')
#         return format_html('<span style="color:gray;">❌ Not Verified</span>')
#     verified_badge.short_description = "Status"

#     def category_list(self, obj):
#         return obj.get_college_category_display()
#     category_list.short_description = "Category"

#     def course_count(self, obj):
#         return obj.courses.count()
#     course_count.short_description = "Courses"

#     def total_seats(self, obj):
#         return sum(c.total_seats for c in obj.courses.all())
#     total_seats.short_description = "Total Seats"

#     def available_seats(self, obj):
#         return sum(c.available_seats for c in obj.courses.all())
#     available_seats.short_description = "Available Seats"

#     def view_site(self, obj):
#         url = reverse('college-detail', args=[obj.pk])
#         return format_html('<a href="{}" target="_blank">🔗 View Site</a>', url)
#     view_site.short_description = "View"

#     @admin.action(description="✅ Approve selected colleges")
#     def approve_college(self, request, queryset):
#         updated = queryset.update(verified=True)
#         self.message_user(request, f"{updated} colleges approved successfully.")


# # ---------- Course ----------
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = (
#         'name', 'college', 'category', 'duration',
#         'total_seats', 'admission_completed', 'available_seats',
#         'is_popular', 'is_active'
#     )
#     # 'level' belongs to CourseCategory; filter courses by the related category's level
#     list_filter = ('is_active', 'is_popular', 'category', 'category__level', 'college__state', 'college__district')
#     search_fields = ('name', 'college__college_name')
#     readonly_fields = ('available_seats',)

#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('college', 'category')


# # ---------- Gallery ----------
# @admin.register(CollegeGallery)
# class CollegeGalleryAdmin(admin.ModelAdmin):
#     list_display = ('college', 'image_preview', 'uploaded_at')
#     readonly_fields = ('uploaded_at',)

#     def image_preview(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" width="100" height="60" style="object-fit:cover;border-radius:5px;">', obj.image.url)
#         return "-"
#     image_preview.short_description = "Preview"


# # ---------- Admission Applications ----------
# @admin.register(AdmissionApplication)
# class AdmissionApplicationAdmin(admin.ModelAdmin):
#     list_display = (
#         'student', 'course', 'college_name', 'status',
#         'applied_at', 'consultant'
#     )
#     list_filter = ('status', 'course__college__state', 'course__college__district')
#     search_fields = ('student__email', 'course__name', 'course__college__college_name')
#     readonly_fields = ('applied_at', 'updated_at', 'student', 'course', 'consultant')

#     fieldsets = (
#         ('Application Info', {
#             'fields': ('student', 'course', 'consultant', 'status', 'submitted_documents')
#         }),
#         ('Timestamps', {
#             'fields': ('applied_at', 'updated_at')
#         }),
#     )

#     def college_name(self, obj):
#         return obj.course.college.college_name
#     college_name.short_description = "College"


# # ---------- Course Category ----------
# @admin.register(CourseCategory)
# class CourseCategoryAdmin(admin.ModelAdmin):
#     # CourseCategory doesn't have an `is_active` field; remove it from display
#     list_display = ('name', 'level', 'slug')
#     search_fields = ('name',)
#     list_filter = ('level',)
