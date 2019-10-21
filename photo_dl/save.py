from photo_dl.log import log


def save(img, path):
    if img and img.status_code == 200:
        with open(path, 'wb') as f:
            f.write(img.content)
        return 1
    else:
        log('[error %s]' % path)
        return 0
