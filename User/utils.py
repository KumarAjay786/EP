# from django.conf import settings
# from twilio.rest import Client

# def send_phone_otp(user, otp):
#     if settings.USE_TWILIO:
#         try:
#             client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#             client.messages.create(
#                 body=f"Your verification OTP is {otp}",
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=user.phone,
#             )
#             print(f"✅ OTP sent via Twilio to {user.phone}")
#         except Exception as e:
#             print(f"❌ Twilio error: {e}")
#     else:
#         # Development fallback
#         print(f"📱 (DEV MODE) OTP for {user.phone}: {otp}")
