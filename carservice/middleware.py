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
