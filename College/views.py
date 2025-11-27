from rest_framework import generics, viewsets,permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, CollegeProfile,Event,Gallery,Faculty,Hostel
from .serializers import (
    CollegeProfileSerializer,
    CourseSerializer,
    EventSerializer,
    GallerySerializer,
    FacultySerializer,
    HostelSerializer,
    CollegePublicSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from College import serializers
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter
from .permissions import IsCollegeOwner, IsCollegeOwnerOrReadOnly, IsCollegeAdminOrReadOnly
import django_filters




class CollegeProfileView(generics.RetrieveUpdateAPIView):
    """
    College Profile Setup & Update View
    - GET → Retrieve current college profile
    - PUT/PATCH → Update profile (both initial setup or later edits)
    """

    serializer_class = CollegeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        """Return the logged-in college user's profile."""
        user = self.request.user
        if user.user_type != "college":
            return Response(
                {"detail": "Only college users can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN,
            )

        profile, _ = CollegeProfile.objects.get_or_create(
            user=user,
            defaults={
                "college_name": user.name or f"College_{user.id}",
                "email": user.email,
                "phone": user.phone,
                "country": "",
                "state": "",
                "district": "",
                "address": "",
            },
        )
        return profile

    def get(self, request, *args, **kwargs):
        """Retrieve profile data."""
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """Full update (used when saving setup form)."""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Profile updated successfully."}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """Partial update (used for dashboard edit)."""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Profile updated successfully."}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollegeFilterSet(FilterSet):
    """
    Custom FilterSet for comprehensive college filtering by location, courses, and status.
    
    Supports filtering by:
    - Location: country, state, district
    - Course details: main_stream, degree, level, specialization
    - Status: verified, is_popular, is_featured
    """
    # Location filters
    country = CharFilter(field_name='country', lookup_expr='icontains')
    state = CharFilter(field_name='state', lookup_expr='icontains')
    district = CharFilter(field_name='district', lookup_expr='icontains')
    
    # College info filters
    college_type = CharFilter(field_name='college_type', lookup_expr='exact')
    accreditation_body = CharFilter(field_name='accreditation_body', lookup_expr='icontains')
    
    # Course-related filters
    main_stream = CharFilter(field_name='courses__main_stream', lookup_expr='exact', distinct=True)
    degree = CharFilter(field_name='courses__degree', lookup_expr='exact', distinct=True)
    level = CharFilter(field_name='courses__level', lookup_expr='exact', distinct=True)
    specialization = CharFilter(field_name='courses__specialization', lookup_expr='icontains', distinct=True)
    
    # Status filters
    verified = django_filters.BooleanFilter(field_name='verified')
    is_popular = django_filters.BooleanFilter(field_name='is_popular')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    
    class Meta:
        model = CollegeProfile
        fields = ['country', 'state', 'district', 'college_type', 'accreditation_body', 
                  'main_stream', 'degree', 'level', 'specialization', 'verified', 'is_popular', 'is_featured']


class CollegeListView(generics.ListAPIView):
    """
    List and filter colleges with comprehensive filtering options.
    
    Colleges are automatically categorized by the main_stream of courses they offer.
    A college offering engineering AND medical courses will appear when filtering 
    by either 'engineering' OR 'medical'.
    
    Supported Filters:
    - location: district, state, country (by location)
    - industry: main_stream (engineering, law, finance, medical, arts)
    - course: degree, level, specialization (by course details)
    - status: verified, is_popular, is_featured (by college status)
    - college_type: government, private, autonomous
    - accreditation_body: by accreditation body
    
    Example queries:
    - /api/colleges/list/?district=Chennai
    - /api/colleges/list/?main_stream=engineering&college_type=private
    - /api/colleges/list/?state=Tamil+Nadu&is_popular=true
    - /api/colleges/list/?district=Chennai&main_stream=medical&degree=MBBS
    - /api/colleges/list/?level=undergraduate&specialization=Computer
    - /api/colleges/list/?main_stream=engineering&is_featured=true&verified=true
    - /api/colleges/list/?accreditation_body=AICTE&college_type=private
    """
    serializer_class = CollegeProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CollegeFilterSet
    
    # Search fields
    search_fields = ['college_name', 'country', 'state', 'district', 'about_college', 'accreditation_body']
    
    # Ordering fields
    ordering_fields = ['college_name', 'created_at', 'is_popular', 'is_featured', 'established_year']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return distinct colleges to avoid duplicates when filtering by related course fields.
        """
        return CollegeProfile.objects.distinct()



class CollegePublicDetailView(generics.RetrieveAPIView):
    """Public read-only detail view for a college.

    URL lookup uses the college's `college_code` so public clients can fetch
    details like courses, events, gallery, faculties and hostels in one call.
    """
    serializer_class = CollegePublicSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'college_code'
    lookup_url_kwarg = 'college_code'

    def get_queryset(self):
        # optimize related resource fetching for the public detail view
        return CollegeProfile.objects.select_related('user').prefetch_related(
            'courses', 'events', 'gallery_items', 'faculties', 'hostels'
        )


class CourseViewSet(viewsets.ModelViewSet):
    """
    Manage courses - College admins can only see/edit their own courses
    
    Authenticated college admins can:
    - View only their own courses
    - Create new courses for their college
    - Edit/Delete only their own courses
    
    Other authenticated users can:
    - View all courses (read-only)
    """
    serializer_class = CourseSerializer
    permission_classes = [IsCollegeAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Define filterable fields
    filterset_fields = {
        'level': ['exact'],
        'degree': ['exact'],
        'main_stream': ['exact'],
        'specialization': ['icontains'],
        'college__college_code': ['exact'],
        'college__country': ['icontains'],
        'college__state': ['icontains'],
        'college__district': ['icontains'],
        'fee': ['lte', 'gte'],
    }
    
    # Search fields
    search_fields = ['specialization', 'college__college_name', 'description']
    
    # Ordering fields
    ordering_fields = ['created_at', 'fee', 'duration', 'degree']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return courses based on user type:
        - College admin: Only their own courses
        - Other users: All courses (public view)
        """
        user = self.request.user
        
        if not user or not user.is_authenticated:
            # Unauthenticated users see no courses
            return Course.objects.none()
        
        # If user is a college admin, show only their courses
        if getattr(user, 'user_type', None) == 'college':
            try:
                college = user.college_profile
                return Course.objects.filter(college=college).select_related('college')
            except CollegeProfile.DoesNotExist:
                return Course.objects.none()
        
        # Other authenticated users can see all courses
        return Course.objects.all().select_related('college')

    def create(self, request, *args, **kwargs):
        """
        Create course - Only college admins can create, and only for their college
        """
        user = request.user
        
        # Check if user is a college admin
        if not user or not user.is_authenticated or getattr(user, 'user_type', None) != 'college':
            return Response(
                {'error': 'Only college admins can create courses.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            college = user.college_profile
        except CollegeProfile.DoesNotExist:
            return Response(
                {'error': 'You must have a college profile to create courses.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create course with authenticated user's college
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(college=college)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_update(self, serializer):
        """Ensure college admin can only update their own college's courses"""
        user = self.request.user
        course = self.get_object()
        
        if course.college.user != user:
            raise permissions.PermissionDenied(
                "You can only update courses for your own college."
            )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure college admin can only delete their own college's courses"""
        user = self.request.user
        
        if instance.college.user != user:
            raise permissions.PermissionDenied(
                "You can only delete courses from your own college."
            )
        
        instance.delete()

    @action(detail=False, methods=['get'], url_path='by-college/(?P<college_code>[^/.]+)')
    def by_college(self, request, college_code=None):
        """
        Custom endpoint: Get all courses for a specific college
        Example: /api/courses/by-college/C40B2C92D3/
        """
        college = get_object_or_404(CollegeProfile, college_code=college_code)
        courses = self.get_queryset().filter(college=college)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

# ===== EVENT VIEWSET =====

class EventViewSet(viewsets.ModelViewSet):
    """
    Manage events - College admins can only see/edit their own events
    
    College admins can:
    - View only their own events
    - Create new events for their college
    - Edit/Delete only their own events
    """
    serializer_class = EventSerializer
    permission_classes = [IsCollegeAdminOrReadOnly]

    def get_queryset(self):
        """
        Return events based on user type:
        - College admin: Only their own events
        - Other users: All events (public view)
        """
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return Event.objects.none()
        
        # If user is a college admin, show only their events
        if getattr(user, 'user_type', None) == 'college':
            try:
                college = user.college_profile
                return Event.objects.filter(college=college)
            except CollegeProfile.DoesNotExist:
                return Event.objects.none()
        
        # Other authenticated users can see all events
        return Event.objects.all()
    
    def perform_create(self, serializer):
        """Create event for authenticated college admin's college"""
        user = self.request.user
        
        if not user or not user.is_authenticated or getattr(user, 'user_type', None) != 'college':
            raise permissions.PermissionDenied(
                "Only college admins can create events."
            )
        
        try:
            college = user.college_profile
            serializer.save(college=college)
        except CollegeProfile.DoesNotExist:
            raise permissions.PermissionDenied(
                "You must have a college profile to create events."
            )
    
    def perform_update(self, serializer):
        """Ensure college admin can only update their own events"""
        user = self.request.user
        event = self.get_object()
        
        if event.college.user != user:
            raise permissions.PermissionDenied(
                "You can only update events for your own college."
            )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure college admin can only delete their own events"""
        user = self.request.user
        
        if instance.college.user != user:
            raise permissions.PermissionDenied(
                "You can only delete events from your own college."
            )
        
        instance.delete()

# ===== GALLERY VIEWSET =====

class GalleryViewSet(viewsets.ModelViewSet):
    """
    Manage gallery - College admins can only see/edit their own gallery
    
    College admins can:
    - View only their own gallery items
    - Upload new gallery items for their college
    - Edit/Delete only their own gallery items
    """
    serializer_class = GallerySerializer
    permission_classes = [IsCollegeAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Return gallery items based on user type:
        - College admin: Only their own gallery
        - Other users: All gallery (public view)
        """
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return Gallery.objects.none()
        
        # If user is a college admin, show only their gallery
        if getattr(user, 'user_type', None) == 'college':
            try:
                college = user.college_profile
                return Gallery.objects.filter(college=college)
            except CollegeProfile.DoesNotExist:
                return Gallery.objects.none()
        
        # Other authenticated users can see all gallery
        return Gallery.objects.all()
    
    def perform_create(self, serializer):
        """Create gallery item for authenticated college admin's college"""
        user = self.request.user
        
        if not user or not user.is_authenticated or getattr(user, 'user_type', None) != 'college':
            raise permissions.PermissionDenied(
                "Only college admins can upload gallery items."
            )
        
        try:
            college = user.college_profile
            serializer.save(college=college)
        except CollegeProfile.DoesNotExist:
            raise permissions.PermissionDenied(
                "You must have a college profile to upload gallery items."
            )
    
    def perform_update(self, serializer):
        """Ensure college admin can only update their own gallery items"""
        user = self.request.user
        gallery = self.get_object()
        
        if gallery.college.user != user:
            raise permissions.PermissionDenied(
                "You can only update gallery items from your own college."
            )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure college admin can only delete their own gallery items"""
        user = self.request.user
        
        if instance.college.user != user:
            raise permissions.PermissionDenied(
                "You can only delete gallery items from your own college."
            )
        
        instance.delete()
    
    def create(self, request, *args, **kwargs):
        """Override create to use college from request.user"""
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return super().create(request, *args, **kwargs)

# ===== FACULTY VIEWSET =====

class FacultyViewSet(viewsets.ModelViewSet):
    """
    Manage faculty - College admins can only see/edit their own faculty
    
    College admins can:
    - View only their own faculty members
    - Create new faculty for their college
    - Edit/Delete only their own faculty members
    """
    serializer_class = FacultySerializer
    permission_classes = [IsCollegeAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Return faculty based on user type:
        - College admin: Only their own faculty
        - Other users: All faculty (public view)
        """
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return Faculty.objects.none()
        
        # If user is a college admin, show only their faculty
        if getattr(user, 'user_type', None) == 'college':
            try:
                college = user.college_profile
                return Faculty.objects.filter(college=college)
            except CollegeProfile.DoesNotExist:
                return Faculty.objects.none()
        
        # Other authenticated users can see all faculty
        return Faculty.objects.all()
        title = request.data.get("title", "")
        description = request.data.get("description", "")

        # use logged-in user's college
        user_college = getattr(request.user, "college_profile", None)

        if not user_college:
            return Response({"detail": "User is not associated with any college."}, status=400)

        # Other authenticated users can see all faculty
        return Faculty.objects.all()
    
    def perform_create(self, serializer):
        """Create faculty for authenticated college admin's college"""
        user = self.request.user
        
        if not user or not user.is_authenticated or getattr(user, 'user_type', None) != 'college':
            raise permissions.PermissionDenied(
                "Only college admins can add faculty members."
            )
        
        try:
            college = user.college_profile
            serializer.save(college=college)
        except CollegeProfile.DoesNotExist:
            raise permissions.PermissionDenied(
                "You must have a college profile to add faculty members."
            )
    
    def perform_update(self, serializer):
        """Ensure college admin can only update their own faculty"""
        user = self.request.user
        faculty = self.get_object()
        
        if faculty.college.user != user:
            raise permissions.PermissionDenied(
                "You can only update faculty members from your own college."
            )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure college admin can only delete their own faculty"""
        user = self.request.user
        
        if instance.college.user != user:
            raise permissions.PermissionDenied(
                "You can only delete faculty members from your own college."
            )
        
        instance.delete()

# ===== HOSTEL VIEWSET =====

class HostelListCreateView(generics.ListCreateAPIView):
    """
    List and create hostels - College admins can only see/edit their own hostels
    """
    serializer_class = HostelSerializer
    permission_classes = [IsCollegeAdminOrReadOnly]

    def get_queryset(self):
        """
        Return hostels based on user type:
        - College admin: Only their own hostels
        - Other users: All hostels (public view)
        """
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return Hostel.objects.all()
        
        # If user is a college admin, show only their hostels
        if getattr(user, 'user_type', None) == 'college':
            try:
                college = user.college_profile
                return Hostel.objects.filter(college=college)
            except CollegeProfile.DoesNotExist:
                return Hostel.objects.none()
        
        # Other authenticated users can see all hostels
        return Hostel.objects.all()
    
    def perform_create(self, serializer):
        """Create hostel for authenticated college admin's college"""
        user = self.request.user
        
        if not user or not user.is_authenticated or getattr(user, 'user_type', None) != 'college':
            raise permissions.PermissionDenied(
                "Only college admins can create hostels."
            )
        
        try:
            college = user.college_profile
            serializer.save(college=college)
        except CollegeProfile.DoesNotExist:
            raise permissions.PermissionDenied(
                "You must have a college profile to create hostels."
            )

class HostelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete hostels - College admins can only edit their own
    """
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsCollegeAdminOrReadOnly]
    
    def perform_update(self, serializer):
        """Ensure college admin can only update their own hostels"""
        user = self.request.user
        hostel = self.get_object()
        
        if hostel.college.user != user:
            raise permissions.PermissionDenied(
                "You can only update hostels from your own college."
            )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure college admin can only delete their own hostels"""
        user = self.request.user
        
        if instance.college.user != user:
            raise permissions.PermissionDenied(
                "You can only delete hostels from your own college."
            )
        
        instance.delete()


class HostelImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # 🔹 Check image
        if "image" not in request.FILES:
            return Response({"error": "No image provided"}, status=400)

        image = request.FILES["image"]

        # 🔹 College ID
        college_id = request.data.get("college")
        if not college_id:
            return Response({"error": "College ID not provided"}, status=400)

        # 🔹 Check college exists
        try:
            college = CollegeProfile.objects.get(id=college_id)
        except CollegeProfile.DoesNotExist:
            return Response({"error": "College not found"}, status=404)

        # 🔹 Check user owns college
        if request.user != college.user:
            return Response({"error": "Permission denied"}, status=403)

        # 🔹 Generate safe filename
        import uuid
        extension = image.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"

        # 🔹 Save file
        path = default_storage.save(f"hostels/{college.id}/{filename}", image)
        image_url = default_storage.url(path)

        # 🔹 Make full URL
        full_url = request.build_absolute_uri(image_url)

        return Response({"image_url": full_url}, status=201)

class FilterOptionsAPIView(APIView):
    """
    Returns all dropdown options OR specific filter options dynamically.
    """

    def get_filter_data(self):
        """Collect all filter values in one place to reuse."""
        countries = CollegeProfile.objects.values_list("country", flat=True).distinct()
        states = CollegeProfile.objects.values_list("state", flat=True).distinct()
        districts = CollegeProfile.objects.values_list("district", flat=True).distinct()

        accreditation = (
            CollegeProfile.objects
            .exclude(accreditation_body__isnull=True)
            .exclude(accreditation_body__exact="")
            .values_list("accreditation_body", flat=True)
            .distinct()
        )

        course_levels = [c[0] for c in Course.COURSE_LEVEL_CHOICES]
        main_streams = [c[0] for c in Course.MAIN_STREAM_CHOICES]
        degrees = [c[0] for c in Course.DEGREE_CHOICES]

        specializations = (
            Course.objects
            .exclude(specialization__isnull=True)
            .exclude(specialization__exact="")
            .values_list("specialization", flat=True)
            .distinct()
        )

        return {
            "countries": list(countries),
            "states": list(states),
            "districts": list(districts),
            "accreditation_bodies": list(accreditation),
            "course_levels": course_levels,
            "main_streams": main_streams,
            "degrees": degrees,
            "specializations": list(specializations),
        }

    def get(self, request, filter_name=None):
        all_filters = self.get_filter_data()

        # If /filters/ → return all
        if filter_name is None:
            return Response(all_filters)

        # If /filters/<filter_name>/ → return only that filter
        if filter_name not in all_filters:
            return Response(
                {"error": f"'{filter_name}' is not a valid filter"},
                status=400
            )

        return Response({filter_name: all_filters[filter_name]})
