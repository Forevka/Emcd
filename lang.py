
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
        
