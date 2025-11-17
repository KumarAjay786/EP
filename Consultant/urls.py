from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConsultantListView.as_view(), name='consultant-list'),
    path('create/', views.ConsultantCreateView.as_view(), name='consultant-create'),
    path('<int:pk>/', views.ConsultantDetailView.as_view(), name='consultant-detail'),
    path('<int:pk>/approve/', views.ConsultantApprovalView.as_view(), name='consultant-approve'),
]
