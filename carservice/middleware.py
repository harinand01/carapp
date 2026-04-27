import requests
from carservice.utils import log_activity, get_client_ip

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        ip = get_client_ip(request)
        username = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_activity(f"Error ({username}): {str(exception)} from {ip}")
        # Return None to let Django's default exception handling take over.
        return None

class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate the response
        response = self.get_response(request)
        
        # Optimization: do not log requests for static or media files
        if request.path.startswith('/static') or request.path.startswith('/media'):
            return response
            
        # Extract required fields
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else "anonymous"
        ip_address = request.META.get('REMOTE_ADDR', '')
        path = request.path
        method = request.method
        status_code = response.status_code
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Create JSON object containing the above fields
        data = {
            "user": user,
            "ip_address": ip_address,
            "path": path,
            "method": method,
            "status_code": status_code,
            "user_agent": user_agent,
        }

        # Send this data to the mini SOC API
        try:
            requests.post("https://YOUR-SOC-URL/api/receive-log/", json=data, timeout=1)
        except Exception:
            # If sending fails, ignore the error (do not break the app)
            pass
            
        return response
