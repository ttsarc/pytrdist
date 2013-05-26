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
    return {'page': page}


@register.inclusion_tag('common/part-flatpage.html')
def show_flatpage(**kwargs):
    url = kwargs.get('url')
    show_title = kwargs.get('show_title', True)
    div_class = kwargs.get('div_class', None)
    print(show_title)
    try:
        page = FlatPage.objects.get(url__exact=url)
    except FlatPage.DoesNotExist:
        page = None
    return {
        'page': page,
        'show_title': show_title,
        'div_class': div_class,
    }
