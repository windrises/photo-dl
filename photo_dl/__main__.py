import sys
import getopt
import signal
from photo_dl.parse import parse
from photo_dl.download import download


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

    signal.signal(signal.SIGINT, handler=handler)
    albums = parse(args[0])
    if len(albums) == 0:
        return
    download(albums)


def handler(signum, frame):
    from photo_dl.request import set_signal
    print('KeyboardInterrupt')
    set_signal()
    sys.exit()


if __name__ == '__main__':
    main()
