def _parse_referer(request):
    ref = request.META.get('HTTP_REFERER')
    if ref:
        host = request.META.get('HTTP_HOST')
        if host and not any(d in ref for d in (host, "pore.savukoski.name")):
            return ref

class ReturnURLMiddleware(object):
    def process_response(self, request, response):
        ref = _parse_referer(request)
        if ref:
            response.set_cookie('return', ref)
        return response
