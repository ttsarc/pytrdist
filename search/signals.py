# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from documents.models import Document
from seminars.models import Seminar
from search.libs import (update_document_search_data,
                         update_seminar_search_data)


def rebuild_document_search_data(sender, instance, **kwargs):
    update_document_search_data(instance)

post_save.connect(rebuild_document_search_data, sender=Document)


def rebuild_seminar_search_data(sender, instance, **kwargs):
    update_seminar_search_data(instance)

post_save.connect(rebuild_seminar_search_data, sender=Seminar)
