from django.urls import path
from User import views

urlpatterns = [
    # 🔹 Authentication & Registration
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),

    # 🔹 Verification (Email + Phone)
    path('verify-email/', views.VerifyEmailOTPView.as_view(), name='verify-email'),
    path('verify-phone/', views.VerifyPhoneOTPView.as_view(), name='verify-phone'),

    # 🔹 Resend OTPs (Rate Limited)
    path('resend-email-otp/', views.ResendEmailOTPView.as_view(), name='resend-email-otp'),
    path('resend-phone-otp/', views.ResendPhoneOTPView.as_view(), name='resend-phone-otp'),

    # 🔹 Password Management
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', views.PasswordResetRequestView.as_view(), name='forgot-password'),
    path('reset-password-confirm/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    # 🔹 Profile Completion Status
    path('profile-status/', views.CheckProfileStatusView.as_view(), name='profile-status'),
    # 🔹 User Management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/', views.UserListView.as_view(), name='user-list'),
]
