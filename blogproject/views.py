#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/30 18:21
# @File    : views.py
# @Software: PyCharm
import json
import os

import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from blogproject import settings


@csrf_exempt
def upload(request):
    """上传文件"""
    file = request.FILES['upload']
    if not file:
        return None

    # 获取当前时间作为文件名
    extension = os.path.splitext(file.name)[1]
    save_file_name = str(round(time.time() * 1000)) + extension

    # 保存路径
    save_path = os.path.join(settings.MEDIA_ROOT, 'image', save_file_name)

    # 获取服务器ip和端口 例如"http://10.131.71.122:8888"
    host = "http://" + request.environ['HTTP_HOST']
    # 访问路径
    visit_url = os.path.join(host, 'media/image', save_file_name)

    # 将文件写入保存路径
    destination = open(save_path, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return HttpResponse(json.dumps({"uploaded": 1, "url": visit_url}))
