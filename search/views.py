# -*- encoding: utf-8 -*-
# Create your views here.
from search.models import Search
from search.forms import SearchForm
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.conf import settings
from documents.models import Document
from seminars.models import Seminar
from search.libs import create_search_query

def search(request, page=1):
    paged_results = []
    count = 0
    if 'page' in request.GET:
        page = request.GET['page']

    if 'keyword' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = create_search_query(form.cleaned_data['keyword'])
            search_results = Search.objects.filter(text__search=query, status=1).order_by('update_date').all()
            if search_results:
                paginator = Paginator(search_results, settings.ITEMS_PER_PAGE)
                try:
                    paged_results = paginator.page(page)
                    count = paginator.count
                except PageNotAnInteger:
                    raise Http404
                except EmptyPage:
                    raise Http404
                else:
                    results = []
                    print('seach query:' + str(search_results.query) )
                    doc_results = Document.objects.filter(pk__in=[item.model_pk for item in paged_results if item.model=='Document'])
                    for item in doc_results:
                        results.append(item)
                    semi_results = Seminar.objects.filter(pk__in=[item.model_pk for item in paged_results if item.model=='Seminar'])
                    for item in semi_results:
                        results.append(item)
                    results.sort(key=lambda x: x.update_date, reverse=True)
                    paged_results.object_list = results
    else:
        form = SearchForm()
    return render_to_response(
            'search/index.html',
            {
                'form': form,
                'count': count,
                'results': paged_results,
            },
            context_instance=RequestContext(request)
    )

