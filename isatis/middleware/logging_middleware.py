import logging
from datetime import datetime

# اسکریپت ذخیره لاگ های برنامه(request_responce.log)
logger = logging.getLogger('django')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_info = 'Anonymous'
        if request.user.is_authenticated:
            user_info = request.user.username

        logger.info(f"Request: {request.method} {request.get_full_path()} by {user_info} at {datetime.now()}")

        response = self.get_response(request)

        logger.info(f"Response: {response.status_code} by {user_info} at {datetime.now()}")

        return response
