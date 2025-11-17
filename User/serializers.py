from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from User.models import EmailOTP, PhoneOTP, PreRegistration, PreEmailOTP, PrePhoneOTP
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

User = get_user_model()

# -----------------------------
# TOKEN HELPER FUNCTION
# -----------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# -----------------------------
# USER SERIALIZER
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_type', 'phone', 'email_verified', 'phone_verified', 'verified', 'is_profile_complete' ]
        read_only_fields = ['id', 'email_verified', 'phone_verified', 'verified','is_profile_complete' ]


# -----------------------------
# REGISTRATION SERIALIZER
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password2', 'user_type', 'phone']
        # name is optional at model level; require it conditionally in validate()
        extra_kwargs = {
            'name': {'required': False},
        }

    def validate(self, attrs):
        errors = {}

        if attrs['password'] != attrs['password2']:
            errors['password'] = "Passwords don't match."

        if attrs['user_type'] in ['admin', 'counsellor']:
            errors['user_type'] = "You cannot register as admin or counsellor."

        # Check if a verified user already exists with this email
        if User.objects.filter(email=attrs['email'], verified=True).exists():
            errors['email'] = "A verified account already exists with this email address."

        # Check if a verified user already exists with this phone number
        if attrs.get('phone') and User.objects.filter(phone=attrs['phone'], verified=True).exists():
            errors['phone'] = "A verified account already exists with this phone number."

        # Require name for students and consultants
        if attrs['user_type'] in ['student', 'consultant'] and not attrs.get('name'):
            errors['name'] = "Name is required for students and consultants."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        # Create a PreRegistration entry, send OTPs for email and phone
        pre = PreRegistration.objects.create(
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            user_type=validated_data.get('user_type')
        )
        pre.set_password(password)

        # create and send pre-registration email OTP
        pre_email_otp = PreEmailOTP.objects.create(pre=pre)
        email_otp = pre_email_otp.generate_otp()
        send_mail(
            "Email Verification OTP",
            f"Hi {pre.email}, your registration email OTP is: {email_otp}",
            settings.DEFAULT_FROM_EMAIL,
            [pre.email],
            fail_silently=True,
        )

        # create and send pre-registration phone OTP if phone provided
        if pre.phone:
            pre_phone_otp = PrePhoneOTP.objects.create(pre=pre)
            phone_otp = pre_phone_otp.generate_otp()
            print(f"🔁 Pre-registration phone OTP for {pre.phone}: {phone_otp}")

        # Return the pre-registration token so frontend can pass it back during verification
        return {'pre_token': str(pre.token), 'message': 'Pre-registration created. Verify email and phone with OTPs.'}


# -----------------------------
# LOGIN SERIALIZER
# -----------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = obj.get('user')
        return get_tokens_for_user(user) if user else None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.email_verified and not user.phone_verified:
            raise serializers.ValidationError("Please verify your email and phone number before logging in.")
        elif not user.email_verified:
            raise serializers.ValidationError("Please verify your email first.")
        elif not user.phone_verified:
            raise serializers.ValidationError("Please verify your phone number first.")

        attrs['user'] = user
        return attrs


# -----------------------------
# CHANGE PASSWORD SERIALIZER
# -----------------------------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# -----------------------------
# PASSWORD RESET REQUEST SERIALIZER
# -----------------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        # Remove old unverified OTPs
        from User.models import EmailOTP
        EmailOTP.objects.filter(user=user, verified=False).delete()

        # Create new OTP for password reset
        otp_obj = EmailOTP.objects.create(user=user)
        otp = otp_obj.generate_otp()

        # Send OTP via email
        subject = "Password Reset OTP"
        message = f"Hi {user.email}, your OTP for password reset is: {otp}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return {"message": "Password reset OTP sent to your email."}


# -----------------------------
# PASSWORD RESET CONFIRM SERIALIZER
# -----------------------------
class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")

        email = attrs.get("email")
        otp = attrs.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_obj = EmailOTP.objects.filter(user=user, otp=otp).last()
            if not otp_obj or not otp_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired OTP.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        attrs["user"] = user
        attrs["otp_obj"] = otp_obj
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        otp_obj = self.validated_data["otp_obj"]
        new_password = self.validated_data["new_password"]

        # Mark OTP as verified
        otp_obj.verified = True
        otp_obj.save()

        # Reset password
        user.set_password(new_password)
        user.save()

        return {"message": "Password has been reset successfully."}



# -----------------------------
# VERIFY EMAIL OTP SERIALIZER
# -----------------------------
class VerifyEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        try:
            user = User.objects.get(email=email)
            otp_obj = EmailOTP.objects.filter(user=user, otp=otp).last()
            if not otp_obj or not otp_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired OTP.")
        except User.DoesNotExist:
            # check most recent pre-registration for this email (users may re-initiate registration)
            pre = PreRegistration.objects.filter(email=email).order_by('-created_at').first()
            if not pre:
                raise serializers.ValidationError("User not found and no pending registration for this email.")

            # optional: reject very old pre-registrations (e.g., older than 7 days)
            if (timezone.now() - pre.created_at).total_seconds() > 7 * 24 * 3600:
                raise serializers.ValidationError("No recent pending registration found for this email. Please register again.")

            otp_obj = PreEmailOTP.objects.filter(pre=pre, otp=otp).last()
            if not otp_obj or not otp_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired OTP for pre-registration.")
        # attach either user or pre-registration to attrs
        if 'user' in locals():
            attrs['user'] = user
            attrs['otp_obj'] = otp_obj
        else:
            attrs['pre'] = pre
            attrs['otp_obj'] = otp_obj
        return attrs

    def save(self, **kwargs):
        # if verifying existing user
        if 'user' in self.validated_data:
            user = self.validated_data['user']
            otp_obj = self.validated_data['otp_obj']
            otp_obj.verified = True
            otp_obj.save()
            user.email_verified = True
            user.update_verification_status()
            user.save()
            return {"message": "Email verified successfully."}
        # else handle pre-registration
        pre = self.validated_data['pre']
        otp_obj = self.validated_data['otp_obj']
        otp_obj.verified = True
        otp_obj.save()
        pre.email_verified = True
        pre.save(update_fields=['email_verified'])

        # if both verified, finalize registration
        if pre.is_fully_verified():
            # create actual user
            user = User.objects.create(
                email=pre.email,
                name=pre.name,
                phone=pre.phone,
                user_type=pre.user_type,
                is_active=True,
            )
            # set hashed password directly
            user.password = pre.password_hash
            user.email_verified = True
            user.phone_verified = True
            user.verified = True
            user.save()
            # cleanup pre-registration
            PreEmailOTP.objects.filter(pre=pre).delete()
            PrePhoneOTP.objects.filter(pre=pre).delete()
            pre.delete()
            return {"message": "Email verified and account created successfully.", "email": user.email}
        return {"message": "Email verified for pending registration. Complete phone verification to finish registration."}


# -----------------------------
# VERIFY PHONE OTP SERIALIZER
# -----------------------------
class VerifyPhoneOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get('phone')
        otp = attrs.get('otp')
        try:
            user = User.objects.get(phone=phone)
            otp_obj = PhoneOTP.objects.filter(user=user, otp=otp).last()
            if not otp_obj or not otp_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired OTP.")
        except User.DoesNotExist:
            # try most recent pre-registration by phone
            pre = PreRegistration.objects.filter(phone=phone).order_by('-created_at').first()
            if not pre:
                raise serializers.ValidationError("User not found and no pending registration for this phone.")

            # optional expiry: reject stale pre-registrations older than 7 days
            if (timezone.now() - pre.created_at).total_seconds() > 7 * 24 * 3600:
                raise serializers.ValidationError("No recent pending registration found for this phone. Please register again.")

            otp_obj = PrePhoneOTP.objects.filter(pre=pre, otp=otp).last()
            if not otp_obj or not otp_obj.is_valid():
                raise serializers.ValidationError("Invalid or expired OTP for pre-registration.")
        # attach either user or pre-registration
        if 'user' in locals():
            attrs['user'] = user
            attrs['otp_obj'] = otp_obj
        else:
            attrs['pre'] = pre
            attrs['otp_obj'] = otp_obj
        return attrs

    def save(self, **kwargs):
        # existing user flow
        if 'user' in self.validated_data:
            user = self.validated_data['user']
            otp_obj = self.validated_data['otp_obj']
            otp_obj.verified = True
            otp_obj.save()
            user.phone_verified = True
            user.update_verification_status()
            user.save()
            return {"message": "Phone number verified successfully."}

        # pre-registration flow
        pre = self.validated_data['pre']
        otp_obj = self.validated_data['otp_obj']
        otp_obj.verified = True
        otp_obj.save()
        pre.phone_verified = True
        pre.save(update_fields=['phone_verified'])

        # finalize if fully verified
        if pre.is_fully_verified():
            user = User.objects.create(
                email=pre.email,
                name=pre.name,
                phone=pre.phone,
                user_type=pre.user_type,
                is_active=True,
            )
            user.password = pre.password_hash
            user.email_verified = True
            user.phone_verified = True
            user.verified = True
            user.save()
            PreEmailOTP.objects.filter(pre=pre).delete()
            PrePhoneOTP.objects.filter(pre=pre).delete()
            pre.delete()
            return {"message": "Phone verified and account created successfully.", "email": user.email}
        return {"message": "Phone verified for pending registration. Complete email verification to finish registration."}


# -----------------------------
# RESEND EMAIL OTP SERIALIZER
# -----------------------------
class ResendEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        if user.email_verified:
            raise serializers.ValidationError("Email is already verified.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        EmailOTP.objects.filter(user=user, verified=False).delete()
        otp_obj = EmailOTP.objects.create(user=user)
        otp = otp_obj.generate_otp()

        subject = "Resend Email Verification OTP"
        message = f"Hi {user.email}, your new email OTP is: {otp}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return {"message": "New email OTP sent successfully."}


# -----------------------------
# RESEND PHONE OTP SERIALIZER
# -----------------------------
class ResendPhoneOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        try:
            user = User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this phone number.")
        if user.phone_verified:
            raise serializers.ValidationError("Phone number already verified.")
        return value

    def save(self):
        phone = self.validated_data['phone']
        user = User.objects.get(phone=phone)
        PhoneOTP.objects.filter(user=user, verified=False).delete()
        otp_obj = PhoneOTP.objects.create(user=user)
        otp = otp_obj.generate_otp()
        print(f"🔁 Resent OTP for {user.phone}: {otp}")
        return {"message": "New phone OTP sent successfully."}
