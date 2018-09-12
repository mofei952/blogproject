#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/10 18:52
# @File    : decorators.py
# @Software: PyCharm
from django.shortcuts import redirect
from django.urls import reverse

from blog.middleware import current_request


def login_required(func):
    def inner(*args, **kwargs):
        request = current_request()
        if 'user' not in request.session:
            return redirect(reverse('blog:login'))
        return func(*args, **kwargs)
    return inner
