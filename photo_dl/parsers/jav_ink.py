from photo_dl.request import request


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
            for page in range(int(pages)):
                html = request('%s/page/%d/' % (category_url, page))
                albums.extend(html.xpath('//*[@id="infinite-articles"]/li[contains(@class, "post")]/a/@href'))
        return albums

    def album2photos(self, album_url):
        photos = []
        album_html = request(album_url)
        album_id = album_html.xpath('//article/div/@id')
        if not album_id:
            return {'error': {'url': album_url, 'info': 'not supported'}}
        album_id = album_id[0]
        if album_id in self.album_flag:
            return
        self.album_flag[album_id] = 1

        album_name = album_html.xpath('//*[contains(@class, "article-title")]/text()')[0]
        photos_html = album_html.xpath('//*[@class="gallery-item"]')
        for photo_html in photos_html:
            photo_url = photo_html.xpath('.//a/@href')[0]
            photo_name = photo_url[photo_url.rfind('/') + 1:]
            photos.append({'photo_url': photo_url, 'photo_name': photo_name})
        album = {'parser_name': self.parser_name, 'album_name': album_name, 'photos': photos}
        return album

    def url2albums(self, url):
        albums_url = []
        if '/category/' in url or '/?s=' in url:
            albums_url.extend(self.category2albums(url))
        else:
            albums_url.append(url)

        albums = []
        for album_url in albums_url:
            albums.append(self.album2photos(album_url))
        return albums
