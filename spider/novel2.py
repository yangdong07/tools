

# -*- coding: utf-8 -*-

import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pymongo import MongoClient


client = MongoClient()
collection = client.spider.novel

# start_url = 'http://www.cangqionglongqi.com/guanjuyipin/349402.html'


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def crawl(name, author, start_url, count=0):
    page_url = start_url

    while count < 5000:
        resp = requests.get(page_url)
        # soup = BeautifulSoup(resp.content, 'lxml')
        soup = BeautifulSoup(resp.content, 'html.parser')

        try:
            chapter = soup.find('div', id='box_con')
            title = chapter.find('h1').get_text().strip()
            content = soup.find(id='content').get_text()
            # 从全局找一下，比从局部找容错率高
            # x = soup.find('div', class_='bottom')
            # next_page = soup.find('a', text='下一章').get('href')

            next_page = ''
            for a in soup.find_all('a'):
                if a.get("href", '').endswith('html'):
                    next_page = a.get('href')
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

            if count % 10 == 0:
                print(count, title, next_page_url)

            count += 1
        except AttributeError as e:
            print('stop @', count, page_url)
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
    # name = '官居一品'
    # author = '三戒大师'
    # start_url = 'http://www.cangqionglongqi.com/guanjuyipin/350323.html'
    # crawl(name, author, start_url, count=916)
    make_txt('官居一品')

'''
第916个， 350323 错误，疑似是乱码的问题。。。。。 用html.parser 可以找出来。 用 lxml找不出来。 前者找出 next_page的 "下一章"是乱码。

这种方法还是有很多问题的。。。从第九百多章就开始有乱码。

考虑解决方法：换不同的源，进行修复


'''
