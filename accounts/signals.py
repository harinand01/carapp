from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from carservice.utils import log_activity, send_log, get_client_ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    message = f"User login success (user: {user.username}) from {ip}"
    log_activity(message)
    send_log("LOGIN_SUCCESS", ip, user.username)

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    username = credentials.get('username', 'Unknown')
    message = f"Failed password (user: {username}) from {ip}"
    log_activity(message)
    send_log("LOGIN_FAILED", ip, username)
