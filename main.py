from services.google_translation_service import GoogleTranslationService
from services.hatena_service import HatenaService
from services.ms_text_analytics_service import MsTextAnalyticsService
from functools import reduce


def get_sentiments_from_url(url):
    entry_data = HatenaService.get_hatena_entry_by_url(url)
    comments = HatenaService.get_comments_by_entry(entry_data)

    translated_texts = GoogleTranslationService.get_translated_texts(comments)

    analytics_data = MsTextAnalyticsService.get_data(translated_texts)
    documents = analytics_data["documents"]
    return documents


def calc_rank_point(book_mark_count, sentiment):
    return book_mark_count * sentiment

data = HatenaService.get_hotentry('it')
items = data['rdf:RDF']['item']
for item in items:
    sentiments = get_sentiments_from_url(item['link'])
    item['sentiment'] = reduce(lambda a, sentiment: a + float(sentiment['score']), sentiments, 0) / len(sentiments)
    item['point'] = calc_rank_point(int(item['hatena:bookmarkcount']), item['sentiment'])

print('ブックマーク数でソート')
items = sorted(items, key=lambda item: int(item['hatena:bookmarkcount']), reverse=True)
for i, item in enumerate(items):
    print('POINT: {}, ブックマーク数: {}, ネガポジ度 {}, {}位, {}, link[{}]'
          .format(item['point'], item['hatena:bookmarkcount'], item['sentiment'], i + 1, item['title'], item['link']))
print('\n\n')
print('ブックマーク数とネガポジ度の統合ランキング')
items = sorted(items, key=lambda item: item['point'], reverse=True)
for i, item in enumerate(items):
    print('POINT: {}, ブックマーク数: {}, ネガポジ度 {}, {}位, {}, link[{}]'
          .format(item['point'], item['hatena:bookmarkcount'], item['sentiment'], i + 1, item['title'], item['link']))
