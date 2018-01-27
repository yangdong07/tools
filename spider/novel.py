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


def crawl(start_url):
    page_url = start_url
    count = 0

    while count < 5000:
        count += 1
        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.content, 'lxml')

        try:
            chapter = soup.find('div', class_='content')
            title = chapter.find('h1').get_text()
            content = chapter.find(id='content').get_text()

            # 从全局找一下，比从局部找容错率高
            next_page = soup.find('a', text='下一章').get('href')
            next_page_url = urljoin(start_url, next_page)

            data = {
                'name': name,
                'author': author,
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


def fix():
    for doc in collection.find({'content': ''}):
        print(doc['url'])
        resp = requests.get(doc['url'])
        soup = BeautifulSoup(resp.content, 'lxml')
        content = soup.find(id='content').get_text()
        doc.update(content=content)
        collection.replace_one({'_id': doc['_id']}, doc)

    # 第一次缺少书名和作者名作为index，添加上
    # collection.update_many({}, {'$set': {'name': '我要做皇帝', 'author': '要离刺荆轲'}})
    # collection.create_index({'name': 1, 'author': 1})


def make_txt(name):
    file_name = name + '.txt'
    with open(file_name, 'w') as f:
        f.write(file_name + '\n')
        # 找出全部，按count排序
        for doc in collection.find({'name': name}).sort('count'):
            f.write('\n\n' + doc['title'] + '\n\n')
            f.write(doc['content'])


if __name__ == '__main__':
    make_txt('我要做皇帝')