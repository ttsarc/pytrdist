# -*- encoding: utf-8 -*-
from django import template
from django.contrib.flatpages.models import FlatPage
register = template.Library()

@register.inclusion_tag('sidebar/part-flatpage.html')
def show_flatpage_sidebar(**kwargs):
    url = kwargs.get('url')
    try:
        page = FlatPage.objects.get(url__exact=url)
    except FlatPage.DoesNotExist:
        page = None
    return { 'page': page }

@register.inclusion_tag('common/part-flatpage.html')
def show_flatpage(**kwargs):
    url = kwargs.get('url')
    try:
        page = FlatPage.objects.get(url__exact=url)
    except FlatPage.DoesNotExist:
        page = None
    return { 'page': page }

