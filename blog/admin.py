# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import PostCategory, PostImage, Post
from sorl.thumbnail.admin import AdminImageMixin
from accounts.models import MyUser

class PostAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = ('title', 'update_date', 'status', 'author', )
    search_fields = ('title', 'content')
    raw_id_fields = ('main_img', 'img',)
    #http://djangosnippets.org/snippets/1558/
    def get_form(self, request, obj=None):
        form = super(PostAdmin,self).get_form(request, obj)
        # form class is created per request by modelform_factory function
        # so it's safe to modify
        #we modify the the queryset
        form.base_fields['author'].queryset = form.base_fields['author'].queryset.filter(is_superuser=True)
        return form

admin.site.register(Post, PostAdmin)

class PostCategoryAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = ('name', 'slug', 'sort')
admin.site.register(PostCategory, PostCategoryAdmin)

class PostImageAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = ('title',)

admin.site.register(PostImage, PostImageAdmin)

