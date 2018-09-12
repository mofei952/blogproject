#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/12 16:44
# @File    : comment_count.py
# @Software: PyCharm

# 同步article的comment_count字段
from blog.models import Article

for a in Article.objects.all():
    a.comment_count = a.comment_set.count()
    for c in a.comment_set.all():
        a.comment_count += c.reply_set.count()
    a.save()