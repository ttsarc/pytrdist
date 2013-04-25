# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from documents.models import Document
from seminars.models import Seminar
from search.models import Search
from search.libs import mecab_separate
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        #reset table
        search = Search.objects.all()
        search.delete()
        cursor = connection.cursor()
        table_name = Search._meta.db_table
        cursor.execute('ALTER TABLE '+ str(table_name) +' AUTO_INCREMENT = 1;')
        #Document
        docs = Document.objects.all()
        for doc in docs:
            text_sorces = (
                doc.title,
                str(doc.company),
                doc.catch,
                doc.detail,
                doc.results,
            )
            text = ' '.join( sorce.encode('utf-8') for sorce in text_sorces )
            search, created = Search.objects.get_or_create(model='Document', model_pk=doc.pk)
            search.text = mecab_separate(text)
            search.update_date = doc.update_date
            search.status = doc.status
            search.save()
        #Seminar
        semis = Seminar.objects.all()
        for semi in semis:
            text_sorces = (
                semi.title,
                str(semi.company),
                semi.catch,
                semi.detail,
                semi.target,
                semi.promoter,
                semi.place_name,
                semi.address,
                semi.get_category_display(),
            )
            text = ' '.join( sorce.encode('utf-8') for sorce in text_sorces )
            search, created = Search.objects.get_or_create(model='Seminar', model_pk=semi.pk)
            search.text = mecab_separate(text)
            search.update_date = semi.update_date
            search.status = semi.status
            search.save()

