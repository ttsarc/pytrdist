# -*- coding: utf-8 -*-
import os, time
from django.db import models
from django.utils import timezone
from django.conf import settings
from blog.choices import *
from sorl.thumbnail import ImageField
from trwk.libs.file_utils import normalize_filename

class PostCategory(models.Model):
    name = models.CharField('カテゴリ名', max_length=32)
    slug = models.SlugField('スラッグ')
    sort = models.SmallIntegerField('並び順(大が上)', default=0)
    class Meta:
        verbose_name = "投稿カテゴリー"
        verbose_name_plural = "投稿カテゴリー"
        ordering = ['-sort']
    def __unicode__(self):
        return self.name

class PostImage(models.Model):
    def get_img_uplod_path(self, filename):
        filename = normalize_filename(filename)
        root_path = os.path.join('blog', 'img')
        user_path = os.path.join(root_path, time.strftime('%Y/%m'))
        return os.path.join(user_path, filename)
    img_file = ImageField(
        verbose_name = '画像',
        upload_to = get_img_uplod_path,
        blank = True,
    )
    alt = models.CharField('タイトル', max_length=255)
    class Meta:
        verbose_name = "画像"
        verbose_name_plural = "画像"
    def __unicode__(self):
        return self.alt

class Post(models.Model):
    title =    models.CharField('タイトル', max_length=255)
    slug =     models.SlugField('スラッグ', help_text='URLに使われます。半角英数')
    content =  models.TextField('本文')
    category = models.ManyToManyField(PostCategory, blank=True, verbose_name='カテゴリー')
    img =      models.ManyToManyField(PostImage, blank=True, verbose_name='画像')
    author =   models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='著者', null=True, on_delete=models.SET_NULL)
    date =     models.DateTimeField('更新日', default=timezone.now, blank=True)
    status =   models.SmallIntegerField('公開状態', choices=STATUS_CHOICE, default=1)
    class Meta:
        verbose_name = "投稿"
        verbose_name_plural = "投稿"
        ordering = ['-date']
    def __unicode__(self):
        return self.title
