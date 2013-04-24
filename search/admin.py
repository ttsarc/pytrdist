# -*- coding: utf-8 -*-
from django.contrib import admin
from search.models import Search

class SearchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Search, SearchAdmin)

