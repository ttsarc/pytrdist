# -*- coding: utf-8 -*-
from django.contrib import admin
from documents.models import Document,DocumentDownloadLog, DocumentDownloadCount, DocumentDownloadUser
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'user', 'add_date', 'update_date' )

admin.site.register(Document, DocumentAdmin)

class DocumentDownloadLogAdmin(admin.ModelAdmin):
    readonly_fields = ('download_date',)
    list_display = ('document_title', 'download_date', 'email', 'company_name', )

admin.site.register(DocumentDownloadLog, DocumentDownloadLogAdmin)

class DocumentDownloadCountAdmin(admin.ModelAdmin):
    list_display = ('document','count')
    readonly_fields = ('document',)

admin.site.register(DocumentDownloadCount, DocumentDownloadCountAdmin)

class DocumentDownloadUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'document',)
    readonly_fields = ('document','user','add_date','update_date')

admin.site.register(DocumentDownloadUser, DocumentDownloadUserAdmin)


