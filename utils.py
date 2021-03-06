import itertools
import json
from os import listdir
from os.path import isfile, join, splitext
from typing import Dict

from poeditor_client.client import PoeditorClient


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

def format_rate(rate: int) -> str:
    power = 1000
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E', 7: 'Z'}
    while rate > power:
        rate /= power
        n += 1
    return f'{round(rate, 2)} {power_labels[n]}h/s'


def dict_to_poeditor_locale(data: Dict[str, str], locale: str):
    '''
    [
        {
            "term": "app.name",
            "definition": "TODO List"
        }
    ]
    '''
    return [{"term": term, "definition": translation} for term, translation in data[locale].items()]

async def load_translations(poeditor_id: int, poeditor_token: str,):
    translations = {}

    async with PoeditorClient(poeditor_token, poeditor_id,) as client:
        langs = await client.get_available_languages()
        for lang in langs.result.languages:
            translation_file = await client.get_language_file_url(lang.code)
            translation = await client.download_translation_file(translation_file.result.url)
            translations[lang.code] = json.loads(translation)

    return translations


async def load_translations_from_file():
    translations = {}

    '''async with PoeditorClient(poeditor_token, poeditor_id,) as client:
        langs = await client.get_available_languages()
        for lang in langs.result.languages:
            translation_file = await client.get_language_file_url(lang.code)
            translation = await client.download_translation_file(translation_file.result.url)
            translations[lang.code] = json.loads(translation)
    '''
    path = 'locales/import'
    for f in (f for f in listdir(path) if isfile(join(path, f))):
        ff = open(join(path, f), 'r')
        translations[splitext(f)[0]] = json.loads(ff.read())

    return translations

if __name__ == "__main__":
    from config import texts
    
    file = dict_to_poeditor_locale(texts, 'en')
    f = open('locales/export/en.json', 'w')
    f.write(json.dumps(file))
    f.close()
