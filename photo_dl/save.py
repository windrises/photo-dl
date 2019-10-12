def save(img, path):
    if img.status_code == 200:
        with open(path, 'wb') as f:
            f.write(img.content)
        return 1
    else:
        with open('./error_log.txt', 'a') as f:
            f.write(path + '\n')
        return 0
