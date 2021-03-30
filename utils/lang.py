from loguru import logger
import json

language_map = {
    'ru': "Русский",
    'en': "English",
    'fa': "Persian",
}

# placeholder for langs
texts = {}
reversed_locales = {}

def update_texts(data: dict):
    global texts, reversed_locales
    texts = data
    for lang_code, terms in texts.items():
        reversed_locales[lang_code] = dict((v.lower(), k.lower()) for k,v in terms.items()) # exchange key with values
        
class LangHolder(dict):
    def __init__(self, lang_id: int, lang_code: str,):
        self.lang_id = lang_id
        self.lang_code = lang_code
        self.terms_dict = dict(texts[lang_code]) # copy terms

    def __setitem__(self, key, item):
        self.terms_dict[key] = item

    def __getitem__(self, key):
        translation = self.terms_dict[key]
        if (translation is None or translation == ''):
            logger.warning(f'No translation defined for {key} {self.lang_id}')
            return f'No translation defined\nIf you see this message please contact with support'

        return translation

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.terms_dict[key]

    def clear(self):
        return self.terms_dict.clear()

    def copy(self):
        return self.terms_dict.copy()

    def has_key(self, k):
        return k in self.terms_dict

    def update(self, *args, **kwargs):
        return self.terms_dict.update(*args, **kwargs)

    def keys(self):
        return self.terms_dict.keys()

    def values(self):
        return self.terms_dict.values()

    def items(self):
        return self.terms_dict.items()

    def pop(self, *args):
        return self.terms_dict.pop(*args)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)
