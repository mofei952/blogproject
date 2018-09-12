import re
import urllib

from bs4 import BeautifulSoup
from lxml import etree

import requests
from django.test import TestCase

# Create your tests here.

# 下载贴吧头像
# a='<ul class="pass-portrait-hotrecommend" id="passPortraitHotrecommend" data-hotpor="wildkid-13"><li id="hot-wildkid-1" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/1" data-serie="wildkid" data-num="1"><span class="recommendSpan"></span></li><li id="hot-wildkid-2" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/2" data-serie="wildkid" data-num="2"><span class="recommendSpan"></span></li><li id="hot-wildkid-3" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/3" data-serie="wildkid" data-num="3"><span class="recommendSpan"></span></li><li id="hot-wildkid-4" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/4" data-serie="wildkid" data-num="4"><span class="recommendSpan"></span></li><li id="hot-wildkid-5" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/5" data-serie="wildkid" data-num="5"><span class="recommendSpan"></span></li><li id="hot-wildkid-6" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/6" data-serie="wildkid" data-num="6"><span class="recommendSpan"></span></li><li id="hot-wildkid-7" class="pass-portrait-clearmr"><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/7" data-serie="wildkid" data-num="7"><span class="recommendSpan"></span></li><li id="hot-wildkid-8" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/8" data-serie="wildkid" data-num="8"><span class="recommendSpan"></span></li><li id="hot-wildkid-9" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/9" data-serie="wildkid" data-num="9"><span class="recommendSpan"></span></li><li id="hot-wildkid-10" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/10" data-serie="wildkid" data-num="10"><span class="recommendSpan"></span></li><li id="hot-wildkid-11" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/11" data-serie="wildkid" data-num="11"><span class="recommendSpan"></span></li><li id="hot-wildkid-12" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/12" data-serie="wildkid" data-num="12"><span class="recommendSpan"></span></li><li id="hot-wildkid-13" class="visiHot"><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/13" data-serie="wildkid" data-num="13"><span class="recommendSpan"></span></li><li id="hot-wildkid-14" class="pass-portrait-clearmr"><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/14" data-serie="wildkid" data-num="14"><span class="recommendSpan"></span></li><li id="hot-wildkid-15" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/15" data-serie="wildkid" data-num="15"><span class="recommendSpan"></span></li><li id="hot-wildkid-16" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/16" data-serie="wildkid" data-num="16"><span class="recommendSpan"></span></li><li id="hot-wildkid-17" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/17" data-serie="wildkid" data-num="17"><span class="recommendSpan"></span></li><li id="hot-wildkid-18" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/18" data-serie="wildkid" data-num="18"><span class="recommendSpan"></span></li><li id="hot-wildkid-19" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/19" data-serie="wildkid" data-num="19"><span class="recommendSpan"></span></li><li id="hot-wildkid-20" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/20" data-serie="wildkid" data-num="20"><span class="recommendSpan"></span></li><li id="hot-wildkid-21" class="pass-portrait-clearmr"><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/21" data-serie="wildkid" data-num="21"><span class="recommendSpan"></span></li><li id="hot-wildkid-22" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/22" data-serie="wildkid" data-num="22"><span class="recommendSpan"></span></li><li id="hot-wildkid-23" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/23" data-serie="wildkid" data-num="23"><span class="recommendSpan"></span></li><li id="hot-wildkid-24" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/24" data-serie="wildkid" data-num="24"><span class="recommendSpan"></span></li><li id="hot-wildkid-25" class=""><img src="https://ss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/hotitem/wildkid/25" data-serie="wildkid" data-num="25"><span class="recommendSpan"></span></li></ul>'
# g=re.findall(r'"https://[\w\.\/]+"', a)
# for i in g:
#     print(i)
#     ii = i[i.rindex('/')+1:-1]
#     print(ii)
#     urllib.request.urlretrieve(i[1:-1], '../media/profile_picture/%s.jpg' % (ii))

# 创建pp数据
# from blog.models import ProfilePicture
#
# for i in range(1,26):
#     ProfilePicture.objects.create(image='profile_picture/%d.jpg'%i, is_system=True)

# response = requests.get('http://roll.blog.sina.com.cn/list/eatblog/mszhufu/index.shtml')
# response.encoding = 'gb2312'
# web_data = response.text
# html = etree.HTML(web_data)
# alinks = html.xpath("//ul[@class='list_009']/li/a")
# for alink in alinks:
#     print(alink.text, alink.get('href'))
#     response = requests.get(alink.get('href'))
#     response.encoding = 'utf-8'
#     web_data2 = response.text
#     html2 = etree.HTML(web_data2)
#     div = html2.xpath("//div[@id='sina_keyword_ad_area2']")[0]
#     print(div.text)


# response = requests.get('http://roll.blog.sina.com.cn/list/eatblog/mszhufu/index.shtml')
# response.encoding = 'gb2312'
# web_data = response.text
# soup = BeautifulSoup(web_data, "html.parser")
# ul = soup.find('ul', {'class': 'list_009'})
# alinks = ul.find_all('a')
# for i,alink in enumerate(alinks):
#     if i %2==0:
#         continue
#     print(alink.text, alink.get('href'))
#     response = requests.get(alink.get('href'))
#     response.encoding = 'utf-8'
#     web_data2 = response.text
#     soup2 = BeautifulSoup(web_data2, "html.parser")
#     div = soup2.find('div', {'id':'sina_keyword_ad_area2'})
#     print(div.__str__())

num_pages = 20
display_count = 5
p = display_count//2
for num in range(1,21):
    s = max(num-p,1)
    e = min(num+2*p, num_pages)
    if e-s+1>display_count:
        e-=e-s+1-display_count
    print(num,s, e)