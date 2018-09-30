#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/9 16:45
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from django.urls import path, re_path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('LogoutView', views.LogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:page>', views.IndexView.as_view(), name='index'),
    path('publish_article', views.PublishArticleView.as_view(), name='publish_article'),
    path('article_detail/<int:id>', views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'^user_information/(?P<id>\d+)?', views.UserInformationView.as_view(), name='user_information'),
    path('user_article_manage', views.UserArticleManageView.as_view(), name='user_article_manage'),
    path('user_article_manage/<int:page>', views.UserArticleManageView.as_view(), name='user_article_manage'),
    path('user_notice', views.UserNoticeView.as_view(), name='user_notice'),
    path('user_follow', views.UserFollowView.as_view(), name='user_follow'),
    path('user_followed', views.UserFollowedView.as_view(), name='user_followed'),
    path('publish_comment/<int:article_id>', views.PublishCommentView.as_view(), name='publish_comment'),
    path('modify_user_info', views.ModifyUserInfoView.as_view(), name='modify_user_info'),
    path('profile_picture_list', views.ProfilePictureListView.as_view(), name='profile_picture_list'),
    path('modify_profile_picture', views.ModifyProfilePictureView.as_view(), name='modify_profile_picture'),
    path('notice_list/<str:notice_type_id>', views.NoticeListView.as_view(), name='notice_list'),

    url(r'^ajax_get_article_list/(?P<id>\d+)?', views.ajax_get_article_list, name='ajax_get_article_list'),
    path('ajax_delete_article/<int:id>', views.ajax_delete_article, name='ajax_delete_article'),
    url(r'^ajax_follow/(?P<user_id>\d+)', views.ajax_follow),
    url(r'^ajax_cancel_follow/(?P<user_id>\d+)', views.ajax_cancel_follow),
    path('ajax_reply/<int:comment_id>', views.ajax_reply)
]
