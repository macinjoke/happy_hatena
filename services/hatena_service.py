import urllib.request, urllib.parse, urllib.error
import json
import xmltodict

class HatenaService:

    _ENTRY_END_POINT = 'http://b.hatena.ne.jp/entry/jsonlite/'
    _HOT_ENTRY_END_POINT = 'http://b.hatena.ne.jp/hotentry'

    @classmethod
    def get_hatena_entry_by_url(cls, url):
        params = urllib.parse.urlencode({
            "url": url
        })
        request_url = "{}?{}".format(cls._ENTRY_END_POINT, params)
        result = urllib.request.urlopen(request_url).read()
        data = json.loads(result.decode('utf-8'))
        return data

    @classmethod
    def get_comments_by_entry(cls, entry):
        comments = list(filter(
            lambda comment: comment,
            map(lambda bm: bm['comment'], entry['bookmarks'])
        ))
        return comments

    @classmethod
    def get_hotentry(cls, catecory=None):
        if catecory:
            request_url = "{}/{}.rss".format(cls._HOT_ENTRY_END_POINT, catecory)
        else:
            request_url = "{}{}".format(cls._HOT_ENTRY_END_POINT, '?mode=rss')
        result = urllib.request.urlopen(request_url).read()
        data = xmltodict.parse(result.decode('utf-8'))
        return data

