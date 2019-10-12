from photo_dl.config import headers
from photo_dl.config import timeout
from photo_dl.config import max_retries
import requests
from lxml import etree
from requests.adapters import HTTPAdapter


def request(url, html=True):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=max_retries))
    session.mount('https://', HTTPAdapter(max_retries=max_retries))
    response = session.get(url=url, headers=headers, timeout=timeout)
    if html:
        response.encoding = 'utf-8'
        return etree.HTML(response.text)
    return response
