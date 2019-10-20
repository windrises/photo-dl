import sys
import traceback
from photo_dl.log import log
from photo_dl import parsers


def parse(arg):
    albums = []
    print('parsing...')
    input_urls = []
    if arg.find('.txt') != -1:
        with open(arg, 'r') as f:
            input_urls.extend(f.readlines())
    else:
        input_urls.append(arg)
    for input_url in input_urls:
        input_url = input_url.strip()
        try:
            parser = parsers.url2parser(input_url)
            if parser is None:
                print('[error]   %s not supported' % input_url)
                continue
            _albums = parser().url2albums(input_url)
            if len(_albums) == 1 and 'error' in _albums[0]:
                print('[error]   %s %s' % (input_url, _albums[0]['error']['info']))
                continue
            albums.extend(_albums)
            print('\r[succeed] %s' % input_url)
        except SystemExit:
            sys.exit()
        except:
            print('[error]   %s\nCheck the log file for more information' % input_url)
            log('%s\n%s' % (input_url, traceback.format_exc()))
            continue
    return albums
