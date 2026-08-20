from django.utils import timezone
from .models import ActiveUserSession

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.session.session_key:
            session_key = request.session.session_key
            ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:250]

            try:
                ActiveUserSession.objects.update_or_create(
                    session_key=session_key,
                    defaults={
                        'user': request.user,
                        'ip_address': ip,
                        'user_agent': user_agent,
                        'last_activity': timezone.now()
                    }
                )
            except Exception:
                pass

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
