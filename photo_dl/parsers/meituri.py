from photo_dl.request import request
from .__init__ import re


class Meituri:
    def __init__(self):
        self.parser_name = 'meituri'
        self.domain = 'https://www.meituri.com'
        self.album_flag = {}

    def model2albums(self, model_url):
        model_html = request(model_url)
        albums = model_html.xpath('//*[@class="hezi"]//li/a/@href')
        pages = model_html.xpath('//*[@id="pages"]/href')
        if pages:
            pages = list(set(pages))
            for page in pages:
                if '/s/' in page:
                    html = request(self.domain + page)
                    albums.extend(html.xpath('//*[@class="hezi"]//li/a/@href'))
        return albums

    def album2photos(self, album_url):
        photos = []
        pos1 = album_url.find('/a/') + 3
        pos2 = album_url.find('/', pos1)
        album_id = album_url[pos1: pos2]
        if album_id in self.album_flag:
            return
        self.album_flag[album_id] = 1

        album_html = request(album_url)
        num = album_html.xpath('//*[contains(text(), "图片数量")]/text()')[0]
        num = num[num.find('： ') + 2: num.find('P')]

        album_name = album_html.xpath('//title/text()')[0]
        if re.match('.*第.*页.*', album_name):
            album_name = album_name[:album_name.rfind('/') - 1]

        for i in range(1, int(num) + 1):
            photo_name = str(i) + '.jpg'
            photo_url = 'https://ii.hywly.com/a/1/' + album_id + '/' + photo_name
            photos.append({'photo_url': photo_url, 'photo_name': photo_name})
        album = {'parser_name': self.parser_name, 'album_name': album_name, 'photos': photos}
        return album

    def url2albums(self, url):
        albums_url = []
        if '/t/' in url:
            albums_url.extend(self.model2albums(url))
        elif '/a/' in url:
            albums_url.append(url)
        else:
            return [{'error': {'url': url, 'info': 'not supported'}}]

        albums = []
        for album_url in albums_url:
            albums.append(self.album2photos(album_url))
        return albums
