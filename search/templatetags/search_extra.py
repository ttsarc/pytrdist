# -*- encoding: utf-8 -*-<F7>
from django import template
register = template.Library()
from search.forms import SearchForm


@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.simple_tag(takes_context=True)
def search_form(context):
    if 'request' in context and context['request'].GET:
        form = SearchForm(context['request'].GET, auto_id='extra_id_%s')
    else:
        form = SearchForm(auto_id='extra_id_%s')
    return form['keyword']
