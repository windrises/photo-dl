from photo_dl.config import log_file


def log(info):
    with open(log_file, 'a') as file:
        file.write(str(info) + '\n')
