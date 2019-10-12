import os
import sys
import getopt
import traceback
from photo_dl.request import request
from photo_dl.save import save
from photo_dl import parsers


def main():
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    _help = 'assign a url or .txt file which one url one line\n' +\
            '$ photo-get  url\n' +\
            '$ photo-get xxx.txt'
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
    try:
        if arg.find('.txt') != -1:
            with open(arg, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    parser = parsers.url2parser(line)()
                    albums.extend(parser.url2albums(line))
        else:
            parser = parsers.url2parser(arg)()
            albums.extend(parser.url2albums(arg))
    except:
        print('parse error')
        print(traceback.print_exc())
        return

    tot_num = 0
    tot_success = 0
    for album in albums:
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
    print('end')
    print('*' * 50)
    print('total success: %d, total error: %d' % (tot_success, int(tot_num) - tot_success))
    if tot_success < tot_num:
        print('you can try again')


if __name__ == '__main__':
    main()
