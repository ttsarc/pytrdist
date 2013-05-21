# -*- coding: utf-8 -*-
from django.contrib import admin
from seminars.models import Seminar, SeminarEntryLog, SeminarEntryUser
from sorl.thumbnail.admin import AdminImageMixin


class SeminarAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = (
        'title', 'company',
        'user', 'add_date',
        'update_date', 'status')
    list_filter = ('status', )
admin.site.register(Seminar, SeminarAdmin)


class SeminarEntryLogAdmin(admin.ModelAdmin):
    readonly_fields = ('entry_date',)
    list_display = ('seminar_title', 'entry_date', 'email', 'company_name', )

admin.site.register(SeminarEntryLog, SeminarEntryLogAdmin)


class SeminarEntryUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'seminar',)
    readonly_fields = ('seminar', 'user', 'add_date')

admin.site.register(SeminarEntryUser, SeminarEntryUserAdmin)
