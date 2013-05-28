# -*- encoding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from blog.models import Post
from documents.models import Document
from seminars.models import Seminar
from accounts.models import Company


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.update_date


class DocumentSitemap(Sitemap):
    def items(self):
        return Document.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.update_date


class SeminarSitemap(Sitemap):
    def items(self):
        return Seminar.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.update_date


class CompanySitemap(Sitemap):
    def items(self):
        return Company.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.update_date
