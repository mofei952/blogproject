#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/9 16:25
# @File    : forms.py
# @Software: PyCharm

from django import forms

from blog.models import User, Article, Comment


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
    confirm_password = forms.CharField(required=True)

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        error_messages = {
            'content': {
                'required': '内容不能为空'
            }
        }
