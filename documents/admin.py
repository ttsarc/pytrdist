# -*- coding: utf-8 -*-
from documents.models import Document
from django.contrib import admin

class DocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Document, DocumentAdmin)

