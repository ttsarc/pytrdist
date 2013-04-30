# -*- coding: utf-8 -*-
import os, time
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from blog.choices import *
from sorl.thumbnail import ImageField, get_thumbnail
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
    )
    title = models.CharField('タイトル', max_length=255, help_text="管理画面でのラベル、altなどに使われます")
    update_date = models.DateTimeField('更新日', auto_now=True)
    class Meta:
        verbose_name = "画像"
        verbose_name_plural = "画像"
    def __unicode__(self):
        return self.title

class Post(models.Model):
    title =       models.CharField('タイトル', max_length=255)
    slug =        models.SlugField('スラッグ', help_text='URLに使われます。URLの維持とSEOのため手入力してください。半角英数とハイフン')
    content =     models.TextField('本文', help_text='画像にアップしたものを  &lt;!-- img {画像ID} --&gt;  で埋め込むことができます。')
    category =    models.ManyToManyField(PostCategory, blank=True, verbose_name='カテゴリー')
    main_img =    models.ForeignKey(PostImage, blank=True, verbose_name='メイン画像', related_name="post_with_main_img")
    img =         models.ManyToManyField(PostImage, blank=True, verbose_name='画像')
    author =      models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='著者', null=True, on_delete=models.SET_NULL)
    update_date = models.DateTimeField('更新日', default=timezone.now, blank=True)
    add_date =    models.DateTimeField('登録日', auto_now_add=True)
    status =      models.SmallIntegerField('公開状態', choices=STATUS_CHOICE, default=1)
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = "投稿"
        verbose_name_plural = "投稿"
        ordering = ['-add_date']
    def __unicode__(self):
        return self.title

    def content_with_img(self, size=None):
        import re
        if size == None:
            size = settings.POST_THUMBNAIL_SIZE
        format_re='(<!\-\- ?img ?([0-9]+) ?\-\->)'
        content = self.content
        pat = re.compile(format_re)
        embed_tags = pat.findall(self.content)
        if not embed_tags:
            return content
        try:
            embed_imgs = PostImage.objects.filter(pk__in=[ int(img[1]) for img in embed_tags])
        except:
            import sys
            print "Unexpected error:", sys.exc_info()[0]
            return content
        exsists_imgs = {}
        for exsists in embed_imgs:
            exsists_imgs[exsists.pk] = exsists
        for img in embed_tags:
            try:
                tag = img[0]
                pk =  int(img[1])
                img = exsists_imgs[pk]
                thumb = get_thumbnail(img.img_file, size)
                img_tag = '<a href="%s" target="_blank" class="post-thumbnail"><img src="%s" alt="%s" width="%s" height="%s"></a>' % (img.img_file.url, thumb.url, self.title, thumb.width, thumb.height )
            except:
                content = content.replace(tag, '<!-- img error ' + str(pk) + ' -->')
                import sys
                print "Unexpected error:", sys.exc_info()[0]
            else:
                content = content.replace(tag, img_tag)
        return content
