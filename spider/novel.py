# -*- coding: utf-8 -*-

import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pymongo import MongoClient


client = MongoClient()
collection = client.spider.novel

start_url = 'http://www.shuquge.com/txt/848/545887.html'

name = '我要做皇帝'
author = '要离刺荆轲'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


page_url = start_url

count = 0

while count < 5000:
    count += 1
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    try:
        chapter = soup.find('div', class_='content')
        title = chapter.find('h1').get_text()
        content = chapter.find(id='content').get_text()

        # 从全局找一下，比从局部找容错率高
        next_page = soup.find('a', text='下一章').get('href')
        next_page_url = urljoin(start_url, next_page)

        data = {
            'count': count,
            'title': title,
            'content': '\n'.join(content.split()),
            'url': page_url,
            'next_page_url': next_page_url,
        }
        collection.insert(data)
        page_url = next_page_url

    except AttributeError as e:
        print(count, page_url)
        break
