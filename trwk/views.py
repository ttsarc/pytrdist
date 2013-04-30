# -*- encoding: utf-8 -*-
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import Http404,HttpResponse
from django.conf import settings
from django.contrib import messages
from documents.models import Document, DocumentDownloadCount
from seminars.models import Seminar

def trwk_home(request):
    return render_to_response(
        'home.html',
        {
        },
        context_instance=RequestContext(request)
    )
