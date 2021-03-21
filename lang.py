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
        
class Term():
    def __init__(self, term: str, translation: str, lang_id: int):
        self.lang_id = lang_id
        self.term = term
        self.translation = translation

    def format(self, *args, **kwargs) -> 'Term':
        return Term(self.term, self.translation.format(*args, **kwargs), self.lang_id)
    
    def __str__(self,) -> str:
        return self.translation
    
    def __add__(self, other) -> 'Term':
        return Term(self.term, self.translation + other, self.lang_id)



class LangHolder(dict):
    def __init__(self, lang_id: int, lang_code: str,):
        self.lang_id = lang_id
        self.lang_code = lang_code
        self.terms_dict = dict(texts[lang_code]) # copy terms

    def __setitem__(self, key, item):
        self.terms_dict[key] = item

    def __getitem__(self, key) -> Term:
        translation = self.terms_dict[key]
        if (translation is None or translation == ''):
            logger.warning(f'No translation defined for {key} {self.lang_id}')
            return Term(key, 'No translation defined\nIf you see this message please contact with support', self.lang_id)

        return Term(key, translation, self.lang_id)

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

