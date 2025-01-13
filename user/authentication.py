from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

# اسکریپت برای ورود با شماره تلفن و رمز عبور
class PhoneNumberBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        phone_number = kwargs.get('phone_number', username)
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
