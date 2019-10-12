import importlib
import re

parsers = ['meituri']


def url2parser(url):
    for parser in parsers:
        if re.match('.*%s.*' % parser, url):
            module = importlib.import_module('.' + parser, __package__)
            return getattr(module, parser.capitalize())
    return None
