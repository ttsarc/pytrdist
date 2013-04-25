# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from documents.models import Document
from seminars.models import Seminar
from search.models import Search
from search.libs import mecab_separate, update_document_search_data, update_seminar_search_data
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        #reset table
        search = Search.objects.all()
        search.delete()
        cursor = connection.cursor()
        table_name = Search._meta.db_table
        cursor.execute('ALTER TABLE ' + table_name + ' AUTO_INCREMENT = 1;')
        #Document
        docs = Document.objects.all()
        for doc in docs:
            print( str(doc) )
            update_document_search_data(doc)
        #Seminar
        semis = Seminar.objects.all()
        for semi in semis:
            print( str(semi) )
            update_seminar_search_data(semi)

