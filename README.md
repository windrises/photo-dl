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

$ git clone https://github.com/windrises/photo-dl

$ cd photo-dl

$ python setup.py install



## Usage

Assign a url or .txt file (one url per line)

$ photo-dl  url

$ photo-dl xxx.txt

#### Examples

$ photo-dl  https://www.meituri.com/t/1820/

$ photo-dl urls.txt



## Supported sites

Temporarily only supports one website

| site                     | example                         |
| :----------------------- | :------------------------------ |
| https://www.meituri.com/ | https://www.meituri.com/t/1820/ |
|                          | https://www.meituri.com/a/7893/ |
