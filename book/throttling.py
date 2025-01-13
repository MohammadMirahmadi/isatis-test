from rest_framework.throttling import UserRateThrottle

# اسکریپت محدود کردن تعداد درخواست
class IsUserRateThrottle(UserRateThrottle):
    rate = '5/min'

    def allow_request(self, request, view):
        if request.user.is_authenticated and request.user.is_user:
            return super().allow_request(request, view)
        return True
