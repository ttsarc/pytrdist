# -*- encoding: utf-8 -*-
import MeCab
import re
from search.models import Search

#from pdfminer.pdfinterp import PDFResourceManager, process_pdf
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from cStringIO import StringIO
#
#def convert_pdf(path):
#    rsrcmgr = PDFResourceManager()
#    retstr = StringIO()
#    codec = 'utf-8'
#    laparams = LAParams()
#    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#    fp = file(path, 'rb')
#    process_pdf(rsrcmgr, device, fp)
#    fp.close()
#    device.close()
#    str = retstr.getvalue()
#    retstr.close()
#    return str


def mecab_separate(text, separate_char=' ', ignores=None, mecab_option=None):
    if not isinstance(text, str):
        text = text.encode('utf-8')
    if mecab_option is None:
        mecab_option = "-Owakati"
    m = MeCab.Tagger(mecab_option)
    if ignores is None:
        ignores = (
            '.', ',', '/', '■', '…', '=' '、', '。',
            '「', '」', '【', '】', '(', '）', '！',
            '？', '!', '?', '『', '』', '・', '　',
            '※', '*', '、', '_', '＿'
        )
    items = []
    node = m.parseToNode(text)
    while node:
        if node.surface not in ignores:
            #node_text = node.surface.
            #replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
            node_text = re.sub('[\n|\r|\t]', " ", node.surface)
            items.append(node_text)
        node = node.next
    #出現頻度を考慮しないので重複を削除
    items = set(items)
    separated_text = separate_char.join(items)
    separated_text = separated_text.strip()
    #print(separated_text)
    return separated_text


def create_search_query(keyword):
    keyword = keyword.replace('　', ' ')
    if len(keyword) > 2:
        keyword = mecab_separate(keyword)
    keywords = keyword.split(' ')
    query = ' +'.join(keywords)
    query = '+' + query
    #print('query: ' + str(query))
    return query


def update_document_search_data(document):
    d = document
    text_sorces = [
        d.title,
        str(d.company),
        d.catch,
        d.detail,
        d.results,
        #PDFの内容も入れる。重いので停
        #convert_pdf(settings.MEDIA_ROOT + '/' + doc.pdf_file.name),
    ]
    categories = d.category.all()
    if categories:
        cat_names = []
        for cat in categories:
            cat_names.append(cat.name)
        text_sorces.append(' '.join(cat_names))
    text = ' '.join(text_sorces)
    search, created = Search.objects.get_or_create(
        model='Document',
        model_pk=d.pk,
    )
    search.text = mecab_separate(text)
    search.update_date = d.update_date
    search.status = d.status
    search.save()


def update_seminar_search_data(seminar):
    s = seminar
    text_sorces = [
        s.title,
        str(s.company),
        s.catch,
        s.detail,
        s.target,
        s.promoter,
        s.place_name,
        s.address,
    ]
    categories = s.category.all()
    if categories:
        cat_names = []
        for cat in categories:
            cat_names.append(cat.name)
        text_sorces.append(' '.join(cat_names))
    text = ' '.join(text_sorces)
    search, created = Search.objects.get_or_create(
        model='Seminar',
        model_pk=s.pk
    )
    search.text = mecab_separate(text)
    search.update_date = s.update_date
    search.status = s.status
    search.save()
