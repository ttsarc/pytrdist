# -*- encoding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django import template
register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__
