# -*- coding: utf-8 -*-
from django.contrib import admin
from documents.models import Document,DocumentDownloadLog

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'user', 'add_date', 'update_date' )

admin.site.register(Document, DocumentAdmin)

class DocumentDownloadLogAdmin(admin.ModelAdmin):
    readonly_fields = ('download_date',)
    list_display = ('download_date', 'email', 'document_title','company', )

admin.site.register(DocumentDownloadLog, DocumentDownloadLogAdmin)
