import urllib.request, urllib.parse, urllib.error
import json


class HatenaService:

    _END_POINT = "http://b.hatena.ne.jp/entry/jsonlite/"

    @classmethod
    def get_hatena_entry_by_url(cls, url):
        params = urllib.parse.urlencode({
            "url": url
        })
        request_url = "{}?{}".format(cls._END_POINT, params)
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
