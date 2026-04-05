import os
import datetime
import requests

LOG_FILE_PATH = r"C:\soc_logs\logs.txt"

def send_log(event, ip, user=None):
    url = "https://<my-soc-app>/api/logs/"
    timestamp = datetime.datetime.now().isoformat()
    
    payload = {
        "event": event,
        "ip": ip,
        "timestamp": timestamp,
    }
    
    if user:
        payload["user"] = user
        
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"API log forwarding failed: {e}")


def log_activity(message):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        
        # Format the timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append the log
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(f"{message} at [{timestamp}]\n")
    except Exception as e:
        # Fail silently as logging shouldn't break the app, but could print for debug
        print(f"Logging failed: {e}")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    # Optional Enhancement: Allow switching between real IP and simulated IP based on DEBUG mode
    from django.conf import settings
    # Default to True if DEBUG is True for development and testing
    simulate_ip = getattr(settings, 'DEBUG', True) 
    
    if simulate_ip and (ip == '127.0.0.1' or ip is None):
        import random
        # Try to use request session to maintain the same IP across the user's session
        if hasattr(request, 'session'):
            if 'simulated_ip' not in request.session:
                request.session['simulated_ip'] = f"192.168.1.{random.randint(10, 200)}"
            ip = request.session['simulated_ip']
        else:
            ip = f"192.168.1.{random.randint(10, 200)}"
            
    return ip
