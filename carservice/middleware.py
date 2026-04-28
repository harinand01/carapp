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
        print("MIDDLEWARE HIT")  # debug

        response = self.get_response(request)

        # skip unwanted paths
        if (
            request.path.startswith('/static') or
            request.path.startswith('/media') or
            request.path.startswith('/api') or
            request.path.startswith('/detection')
        ):
            return response

        # user
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else "anonymous"

        # real IP fix
        def get_real_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0]
            return request.META.get('REMOTE_ADDR')

        ip = get_real_ip(request)

        # data
        data = {
            "user": user,
            "ip": ip,
            "path": request.path,
            "method": request.method,
            "status": response.status_code,
        }

        try:
            print("Sending log:", data)

            res = requests.post(
                "https://soc-gnvh.onrender.com/api/receive-log/",
                json=data,
                timeout=3
            )

            print("Response:", res.status_code)

        except Exception as e:
            print("ERROR sending log:", e)

        return response