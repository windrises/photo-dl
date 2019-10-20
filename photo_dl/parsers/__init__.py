import re
import importlib


parsers = {'meituri': 'meituri',
           'jav.ink': 'jav_ink'}


def url2parser(url):
    for site, parser in parsers.items():
        if re.match('.*%s.*' % site, url):
            # print(parser.capitalize())
            module = importlib.import_module('.' + parser, __package__)
            return getattr(module, parser.capitalize())
    return None
