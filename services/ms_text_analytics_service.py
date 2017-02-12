import http.client
import urllib.request, urllib.parse, urllib.error, base64
import json
import itertools

from local_setting.api_keys import SUBSCRIPTION_KEY


class MsTextAnalyticsService:

    _HOST_NAME = "westus.api.cognitive.microsoft.com"
    _END_POINT = "/text/analytics/v2.0/sentiment"

    @classmethod
    def get_data(cls, texts):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        }

        documents_template = {
            "language": "en"
        }

        added_dics = map(lambda x, y: {'text': x, 'id': y},
                         texts, itertools.count(1))
        documents = map(lambda x: {**documents_template, **x}, added_dics)

        request = {
            "documents": list(documents)
        }
        request_str = json.dumps(request)

        params = urllib.parse.urlencode({
        })

        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "{}?{}".format(cls._END_POINT, params), request_str, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        parsed_data = json.loads(data.decode("utf-8"))
        return parsed_data
