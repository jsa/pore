from datetime import datetime

from django.conf import settings as django_settings


def base_url(request):
    secure = request.META.get('HTTPS') == "on"

    port_str = request.META.get('SERVER_PORT')
    if port_str and (secure, port_str) not in ((True, "443"), (False, "80")):
        # port defined and non-default
        port = ":%d" % int(port_str)
    else:
        port = None

    return {'BASE_URL': "%s://%s%s"
                        % ("https" if secure else "http",
                           request.META.get('SERVER_NAME', "localhost"),
                           port)}

def settings(request):
    """Makes also all the secrets available in templates, be careful."""
    return {'settings': django_settings}

def now(request):
    return {'now': datetime.now()}
