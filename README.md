# photo-dl

photo-dl is a command-line downloader which helps to crawl photo albums from [Supported sites](#supported-sites)



## Installation

#### Dependencies

- python >= 3.5
- requests >= 2.12.0
- lxml >= 3.7.0

#### Install via Pip

$ pip install --upgrade photo-dl

#### Install from source

$ git clone https://github.com/windrises/photo-dl.git

$ cd photo-dl

$ python setup.py install



## Usage

Assign a url or .txt file (one url per line)

$ photo-dl  url

$ photo-dl xxx.txt

#### Examples

$ photo-dl  https://www.meituri.com/t/1820/

$ photo-dl urls.txt



## Configuration

modify photo_dl/config.py

| configuration | default       |
| :------------ | :------------ |
| headers       | User-Agent... |
| timeout       | 15 sec        |
| max_retries   | 3             |
| log_file      | ./log.txt     |
| threads       | 4             |



## Supported sites

Temporarily only supports two sites

| site                     | feature             | example                                                      |
| :----------------------- | :------------------ | :----------------------------------------------------------- |
| https://www.meituri.com/ | model               | https://www.meituri.com/t/1820/                              |
|                          | album               | https://www.meituri.com/a/7893/                              |
|                          | search              | https://www.meituri.com/search/有村架純                      |
| https://www.jav.ink/     | tag/search/category | https://www.jav.ink/category/graphis-collection-2002-2018/ [NSFW] |
|                          | album               | https://www.jav.ink/graphis-collection-2002-2018/yura-kano-『sweet-memories』vol-2/ [NSFW] |
