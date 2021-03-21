import json
from lang import Term
from typing import Any
from json import JSONEncoder


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Term):
            return obj.translation
        
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def patch_json_encoder(module: Any, json_encoder: JSONEncoder):

    def dumps(data: Any):
        return json_encoder.encode(data,)

    module.dumps = dumps

def patch_payload_generator(module: Any,):
    from aiogram.utils.payload import DEFAULT_FILTER

    def generate_payload(exclude=None, **kwargs):
        """
        Generate payload

        Usage: payload = generate_payload(**locals(), exclude=['foo'])

        :param exclude:
        :param kwargs:
        :return: dict
        """
        if exclude is None:
            exclude = []
        return {key: str(value) for key, value in kwargs.items() if
                key not in exclude + DEFAULT_FILTER
                and value is not None
                and not key.startswith('_')}
    
    module.generate_payload = generate_payload