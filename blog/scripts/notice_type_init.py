#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/12 17:10
# @File    : notice_type_init.py
# @Software: PyCharm
from blog.models import NoticeType

t = '{{user_name}}在你的文章《{{article_title}}》中发表了评论'
NoticeType.objects.create(name=NoticeType.COMMENT_NOTICE, template=t)
t = '{{user_name}}回复了你在文章《{{article_title}}》中发表的评论{{comment_content}}'
NoticeType.objects.create(name=NoticeType.REPLY_NOTICE, template=t)
t = '{{user_name}}在文章《{{article_title}}》中@了你'
NoticeType.objects.create(name=NoticeType.AT_NOTICE, template=t)
t = '{{user_name}}关注了你'
NoticeType.objects.create(name=NoticeType.FOLLOW_NOTICE, template=t)