from photo_dl.config import log_file
import time


def log(info):
    with open(log_file, 'a') as file:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        file.write('%s\n%s\n' % (timestamp, str(info)))
