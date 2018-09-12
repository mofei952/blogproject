#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/12 10:56
# @File    : extra_tags.py
# @Software: PyCharm
from django import template

register = template.Library()

@register.simple_tag
def get_display_page_range(num_pages,num, display_count=5):
    p = display_count // 2
    s = max(num - p, 1)
    e = min(num + 2 * p, num_pages)
    if e - s + 1 > display_count:
        e -= e - s + 1 - display_count
    print(num, s, e)
    return range(s,e+1)