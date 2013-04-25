# -*- encoding: utf-8 -*-
from django.utils.http import urlquote
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

def get_next_url(request):
    if 'next' in request.session and request.session['next']:
        return request.session['next']
    else:
        return False

def set_next_url(request):
    if 'next' in request.GET and request.GET['next'][0] == '/' and request.GET['next'][1] != '/':
        request.session['next'] = urlquote(request.GET['next'])
    elif 'next' in request.session:
        del request.session['next']
    #return request

