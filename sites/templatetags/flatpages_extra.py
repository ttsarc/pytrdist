# -*- encoding: utf-8 -*-
from django import template
from django.contrib.flatpages.models import FlatPage
register = template.Library()

@register.inclusion_tag('sidebar/part-flatpages.html')
def show_flatpage(**kwargs):
    url = kwargs.get('url')
    page = FlatPage.objects.get(url__exact=url)
    return { 'page': page }

