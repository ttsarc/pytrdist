# -*- coding: utf-8 -*-
from django.contrib import admin
from documents.models import (
    DocumentCategory,
    Document, DocumentDownloadLog,
    DocumentDownloadCount, DocumentDownloadUser)
from sorl.thumbnail.admin import AdminImageMixin


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'with_parent_name',
        'parent',
        'sort',
    )
admin.site.register(DocumentCategory, DocumentCategoryAdmin)


class DocumentAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = (
        'title', 'company',
        'user', 'add_date',
        'update_date', 'status')
    list_filter = ('status', )
admin.site.register(Document, DocumentAdmin)


class DocumentDownloadLogAdmin(admin.ModelAdmin):
    readonly_fields = ('download_date',)
    list_display = (
        'document_title', 'download_date',
        'email', 'company_name', )

admin.site.register(DocumentDownloadLog, DocumentDownloadLogAdmin)


class DocumentDownloadCountAdmin(admin.ModelAdmin):
    list_display = ('document', 'count')
    readonly_fields = ('document',)

admin.site.register(DocumentDownloadCount, DocumentDownloadCountAdmin)


class DocumentDownloadUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'document',)
    readonly_fields = ('document', 'user', 'add_date', 'update_date')

admin.site.register(DocumentDownloadUser, DocumentDownloadUserAdmin)
