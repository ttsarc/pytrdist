# -*- encoding: utf-8 -*-
def get_request_addr_or_ip(request):
    ip = request.META.get('REMOTE_HOST')
    if not ip:
        ip = request.META.get('REMOTE_ADDR')
    if not ip:
        ip = 'error'
    return ip

def get_request_ua(request):
    ua = request.META.get('HTTP_USER_AGENT')
    if ua:
        return ua[0:255]
    return 'none'
