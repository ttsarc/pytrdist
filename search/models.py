# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Search(models.Model):
    """
    ALTER TABLE search_search ADD FULLTEXT seach_text(text);
    ALTER TABLE search_search DROP INDEX  seach_text;
    """
    model = models.CharField('モデル', max_length=16)
    model_pk = models.BigIntegerField('モデルID')
    text = models.TextField('検索対象')
    update_date = models.DateTimeField('更新日', default=timezone.now, blank=True)
    status = models.SmallIntegerField('公開状態', choices=((0,0),(1,1)), default=1)
    def __unicode__(self):
        return str(self.model) + ' ' + str(self.model_pk)

    class Meta:
        verbose_name = "検索用データ"
        verbose_name_plural = "検索用データ"
        ordering = ['-update_date']
        unique_together = (("model", "model_pk"),)
