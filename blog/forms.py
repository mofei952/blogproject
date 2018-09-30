#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/9 16:25
# @File    : forms.py
# @Software: PyCharm

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from blog.models import User, Article, Comment, Reply


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'password')
        error_messages = {
            'name': {
                'required': '用户名不能为空'
            },
            'password': {
                'required': '密码不能为空'
            }
        }
        exclude = {

        }

    def clean(self):
        # self._validate_unique = False
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True, error_messages={'required': '确认密码不能为空'})

    class Meta:
        model = User
        fields = ('name', 'password')
        error_messages = {
            'name': {
                'required': '用户名不能为空',
                'unique': '该用户名已经被使用'
            },
            'password': {
                'required': '密码不能为空'
            },
        }

    def clean(self):
        super(RegisterForm, self).clean()
        data = self.cleaned_data
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('两次输入密码不一致')
            # self.add_errors('confirm_password', '两次输入密码不一致')
            # return None
        return self.cleaned_data


class ModifyUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('age', 'sex')
        error_messages = {
            'age': {
                'required': '年龄不能为空'
            },
            'sex': {
                'required': '性别不能为空'
            }
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content')
        error_messages = {
            'title': {
                'required': '标题不能为空'
            },
            'content': {
                'required': '内容不能为空'
            }
        }

    def clean_content(self):
        """为空验证(前端什么都不填提交的content显示为<p>&nbsp;</p>)"""
        content = self.cleaned_data.get('content')
        text = strip_tags(content).replace('&nbsp;', ' ')
        if not text.strip():
            raise ValidationError('内容不能为空')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        error_messages = {
            'content': {
                'required': '内容不能为空'
            }
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content',)
        error_messages = {
            'content': {
                'required': '内容不能为空'
            }
        }
