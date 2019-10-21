import os
from photo_dl.save import save
from photo_dl.request import MultiRequest


def download(albums):    
    print('\ndownloading...')
    tot_num = 0
    tot_success = 0
    tot_skip = 0
    error_flag = 0
    for album in albums:
        if 'error' in album:
            print('[error]   %s %s' % (album['error']['url'], album['error']['info']))
            error_flag = 1
            continue
        parser_name = album['parser_name']
        album_name = album['album_name']
        photos = album['photos']
        folder = os.path.join('./photo-dl', parser_name, album_name.replace('/', ' '))
        if not os.path.isdir(folder):
            os.makedirs(folder)

        urls = []
        for photo in photos:
            path = os.path.join(folder, photo['photo_name'])
            if os.path.exists(path):
                tot_skip += 1
            else:
                urls.append({'url': photo['photo_url'], 'info': {'photo_name': photo['photo_name']}})

        tot_num += len(urls)
        threads = MultiRequest(urls=urls, name=album_name, html_flag=False).run()
        for i, thread in enumerate(threads):
            path = os.path.join(folder, thread.info['photo_name'])
            file = thread.response
            del thread
            tot_success += save(file, path)
        if len(urls):
            print()

    print('end\n')
    print('total success: %d, total error: %d, total skip: %d' % (tot_success, tot_num - tot_success, tot_skip))
    if tot_success < tot_num or error_flag:
        print('\nIt looks like something went wrong. You can try again')
