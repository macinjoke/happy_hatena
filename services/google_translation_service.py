from google.cloud import translate

from local_setting.api_keys import API_KEY


class GoogleTranslationService:

    _API_KEY = API_KEY
    _TRANSLATE_CLIENT = translate.Client(api_key=_API_KEY)

    @classmethod
    def get_translated_texts(cls, orig_texts):
        translated_texts = []
        count = 0
        start_index = 0
        added_num_per_one_comment = 1
        limit_per_one_request = 130
        for i, comment in enumerate(orig_texts):
            # 文字数を数え
            count += len(comment) + added_num_per_one_comment
            # 文字数が制限数を超えたら
            if count >= limit_per_one_request:
                # 元の文字列から翻訳し
                translations = cls._TRANSLATE_CLIENT.translate(orig_texts[start_index:i],
                                                               source_language='ja', target_language='en')
                # 翻訳済みテキストリストに追加する
                translated_texts += (list(map(lambda x: x['translatedText'], translations)))
                # 文字数カウントを初期化し、
                count = 0
                # indexを戻し、ループする
                start_index = i
        # 余ったひとグループを翻訳し
        translations = cls._TRANSLATE_CLIENT.translate(orig_texts[start_index:],
                                                       source_language='ja', target_language='en')
        # 翻訳済みテキストリストに追加する
        translated_texts += (list(map(lambda x: x['translatedText'], translations)))
        return translated_texts
