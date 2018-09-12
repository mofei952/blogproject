#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/11 23:19
# @File    : script1.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup

from blog.models import Article
# url = 'http://roll.blog.sina.com.cn/list/eatblog/mszhufu/index.shtml'
url='http://roll.blog.sina.com.cn/list/eatblog/mszhufu/index_2.shtml'
response = requests.get(url)
response.encoding = 'gb2312'
web_data = response.text
soup = BeautifulSoup(web_data, "html.parser")
ul = soup.find('ul', {'class': 'list_009'})
alinks = ul.find_all('a')
for i,alink in enumerate(alinks):
    if i %2==0:
        continue
    print(alink.text, alink.get('href'))
    response = requests.get(alink.get('href'))
    response.encoding = 'utf-8'
    web_data2 = response.text
    soup2 = BeautifulSoup(web_data2, "html.parser")
    div = soup2.find('div', {'id':'sina_keyword_ad_area2'})
    # print(div.__str__())

    Article.objects.create(title=alink.text,content=div.__str__(), user_id=9)