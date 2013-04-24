# -*- encoding: utf-8 -*-
# Create your views here.
from search.models import Search
from search.forms import SearchForm
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from documents.models import Document
from seminars.models import Seminar
from search.libs import mecab_separate

def _create_search_query(keyword):
    keyword = keyword.replace('　', ' ')
    if len(keyword) > 2:
        keyword = mecab_separate(keyword)
    keywords = keyword.split(' ')
    query = ' +'.join(keywords)
    query = '+' + query
    print('query: ' + str(query))
    return query

def search(request):
    results = []
    if 'keyword' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = _create_search_query(form.cleaned_data['keyword'])
            search_results = Search.objects.filter(text__search=query, status=1).order_by('update_date').all()
            print('query:' + str(search_results.query) )
            doc_results = Document.objects.filter(pk__in=[item.model_pk for item in search_results if item.model=='Document'])
            for item in doc_results:
                results.append(item)
            semi_results = Seminar.objects.filter(pk__in=[item.model_pk for item in search_results if item.model=='Seminar'])
            for item in semi_results:
                results.append(item)
            results.sort(key=lambda x: x.update_date, reverse=True)
    else:
        form = SearchForm()
    return render_to_response(
            'search/index.html',
            {
                'form': form,
                'results':results,
            },
            context_instance=RequestContext(request)
    )

