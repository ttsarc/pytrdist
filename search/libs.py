# -*- encoding: utf-8 -*-
import MeCab
import re
from django.conf import settings
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


def update_item_search_data(item):
    target_text = item.get_search_text()
    search, created = Search.objects.get_or_create(
        model=item.__class__.__name__,
        model_pk=item.pk,
    )
    print("update model:%-10s  pk:%d" % (item.__class__.__name__, item.pk))
    target_text = item.get_search_text()
    search.text = mecab_separate(target_text)
    search.update_date = item.update_date
    search.status = item.status
    search.save()


def get_search_target_models():
    model_list = settings.SEARCH_TARGET_MODELS
    target_models = []
    for target_str in model_list:
        target = target_str.split('.')
        (package, module, class_name) = (
            target[0],
            '.'.join(target[:-1]),
            target[-1])
        target_class = getattr(
            __import__(module, fromlist=[package]),
            class_name)
        target_models.append(target_class)
    return target_models


def update_all_seach_data():
    target_models = get_search_target_models()
    for target in target_models:
        target_items = target.objects.all()
        for item in target_items:
            update_item_search_data(item)
