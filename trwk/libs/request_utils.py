# -*- encoding: utf-8 -*-
import datetime
from django.utils.http import urlquote
from django.utils import timezone
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

def set_recent_checked(request, model, pk):
    time = timezone.make_naive(datetime.datetime.utcnow().replace(tzinfo=timezone.utc), timezone.get_default_timezone()).strftime('%s%f')
    checked_item = { time:
        {
            'model' : model,
            'pk'  :  int(pk),
        }
    }
    if 'checked_items' not in request.session or not isinstance(request.session['checked_items'], dict):
        request.session['checked_items'] = {}
    else:
        checked_items = request.session['checked_items']
        for k,v in checked_items.items():
            if v['model'] == model and v['pk'] == int(pk):
                print(checked_items[k])
                del checked_items[k]
        sorted_checked_items = {}
        for k, v in sorted(checked_items.items(), reverse=True)[0:4]:
            sorted_checked_items[k] = v
        sorted_checked_items.update(checked_item)
        #print(sorted_checked_items)
        request.session['checked_items'] = sorted_checked_items

def get_recent_checked(request):
    if 'checked_items' in request.session:
        return request.session['checked_items']
    return None

