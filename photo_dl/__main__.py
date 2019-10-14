import os
import sys
import getopt
import traceback
from photo_dl.request import request
from photo_dl.save import save
from photo_dl.log import log
from photo_dl import parsers


def main():
    _help = 'Assign a url or .txt file which one url one line\n' +\
            '$ photo-get  url\n' +\
            '$ photo-get xxx.txt'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as e:
        print(e)
        return
    if not opts and not args:
        print(_help)
        return
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print(_help)
        return
    if len(args) > 1:
        print('too much parameters')
        return

    arg = args[0]
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
            print('[succeed] %s' % input_url)
        except:
            print('[error]   %s\nCheck the log file for more information' % input_url)
            log('%s\n%s' % (input_url, traceback.format_exc()))
            continue

    if len(albums) == 0:
        return
    print('\ndownloading...')
    tot_num = 0
    tot_success = 0
    error_flag = 0
    for album in albums:
        if 'error' in album:
            print('[error]   %s %s' % (album['error']['url'], album['error']['info']))
            error_flag = 1
            continue
        parser_name = album['parser_name']
        album_name = album['album_name']
        photos = album['photos']
        print(album_name)
        folder = os.path.join('./photo-dl', parser_name, album_name.replace('/', ' '))
        if not os.path.isdir(folder):
            os.makedirs(folder)
        num = len(photos)
        tot_num += num
        print('total: %dP' % num)
        success = 0
        for i, photo in enumerate(photos):
            path = os.path.join(folder, photo['photo_name'])
            if os.path.exists(path):
                success += 1
                continue
            try:
                file = request(photo['photo_url'], html=False)
            except:
                continue
            success += save(file, path)
            print('\r%d / %s ' % (i + 1, num), end='')
        print()
        print('success: %d, error: %d' % (success, int(num) - success))
        print('-' * 50)
        tot_success += success
    print('end\n')
    print('total success: %d, total error: %d' % (tot_success, int(tot_num) - tot_success))
    if tot_success < tot_num or error_flag:
        print('\nIt looks like something went wrong. You can try again')


if __name__ == '__main__':
    main()
