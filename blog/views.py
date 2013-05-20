# Create your views here.
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from blog.models import Post


def index(request, page=1):
    posts = Post.objects.filter(status=1)
    paged_posts = None
    count = None
    if posts:
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        try:
            paged_posts = paginator.page(page)
            count = paginator.count
        except PageNotAnInteger:
            raise Http404
        except EmptyPage:
            raise Http404

    return render_to_response(
        'blog/index.html',
        {
            'posts': paged_posts,
            'count': count,
        },
        context_instance=RequestContext(request)
    )


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    return render_to_response(
        'blog/detail.html',
        {
            'post': post,
        },
        context_instance=RequestContext(request)
    )
