# -*- encoding: utf-8 -*-
from django import template
from blog.models import Post
register = template.Library()

@register.inclusion_tag('sidebar/part-posts.html')
def show_posts(**kwargs):
    limit = kwargs.get('limit', 5)
    category = kwargs.get('category', None)
    posts = Post.objects.filter(status=1)
    if category:
        posts.filter(category__in=category)
    return { 'posts': posts[0:limit] }


