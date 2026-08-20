from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import ActiveUserSession, LoginLog

def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')[:250] if request else ''
    LoginLog.objects.create(
        user=user,
        username_entered=user.username,
        success=True,
        ip_address=ip,
        user_agent=ua
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')[:250] if request else ''
    username = credentials.get('username', 'Desconocido') if credentials else 'Desconocido'
    LoginLog.objects.create(
        user=None,
        username_entered=username,
        success=False,
        ip_address=ip,
        user_agent=ua
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if request and request.session and request.session.session_key:
        ActiveUserSession.objects.filter(session_key=request.session.session_key).delete()
