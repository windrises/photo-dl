import sys
from photo_dl.request import request
from photo_dl.request import MultiRequest


class Jav_ink:
    def __init__(self):
        self.parser_name = 'jav_ink'
        self.domain = 'https://www.jav.ink'
        self.album_flag = {}

    @staticmethod
    def category2albums(category_url):
        category_url = category_url[:category_url.find('/page/')]
        category_html = request(category_url)
        albums = category_html.xpath('//*[@id="infinite-articles"]/li[contains(@class, "post")]/a/@href')
        pages = category_html.xpath('//*[@class="pages"]/text()')
        if pages:
            pages = pages[0]
            pages = pages[pages.find('of') + 3:]
            urls = []
            for page in range(1, int(pages) + 1):
                urls.append('%s/page/%d/' % (category_url, page))
            urls = [{'url': url} for url in urls]
            threads = MultiRequest(urls=urls, progress=False).run()
            for thread in threads:
                albums.extend(thread.response.xpath('//*[@id="infinite-articles"]\
                                                       /li[contains(@class, "post")]/a/@href'))
                del thread
        return albums

    def album2photos(self, album_url, album_html):
        photos = []
        album_id = album_html.xpath('//article/div/@id')
        if not album_id:
            return {'error': {'url': album_url, 'info': 'not supported'}}
        album_id = album_id[0]
        if album_id in self.album_flag:
            return
        self.album_flag[album_id] = 1

        album_name = album_html.xpath('//*[contains(@class, "article-title")]/text()')
        photos_html = album_html.xpath('//*[@class="gallery-item"]')
        for photo_html in photos_html:
            photo_url = photo_html.xpath('.//a/@href')[0]
            photo_name = photo_url[photo_url.rfind('/') + 1:]
            photos.append({'photo_url': photo_url, 'photo_name': photo_name})
        if len(album_name) == 0:
            album_name = album_url.split('/')[-2]
        else:
            album_name = album_name[0]
        album = {'parser_name': self.parser_name, 'album_name': album_name, 'photos': photos}
        return album

    def url2albums(self, url):
        albums_url = []
        if '/category/' in url or '/?s=' in url:
            albums_url.extend(self.category2albums(url))
        else:
            albums_url.append(url)

        albums = []
        urls = [{'url': url} for url in albums_url]
        threads = MultiRequest(urls=urls, name=url).run()
        for thread in threads:
            try:
                album = self.album2photos(thread.url, thread.response)
                if album is not None:
                    albums.append(album)
            except SystemExit:
                sys.exit()
            except:
                albums.append({'error': {'url': thread.url, 'info': 'parse error'}})
            del thread
        return albums
