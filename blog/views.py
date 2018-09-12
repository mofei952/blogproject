import json

from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import F
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
from django.views import View

from blog.decorators import login_required
from blog.forms import LoginForm, RegisterForm, ArticleForm, CommentForm, ModifyUserInfoForm, ReplyForm
from blog.models import User, Article, Follow, ProfilePicture, ArticleRead, Comment, Notice, NoticeType


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            name = data.get('name')
            password = data.get('password')
            user = User.objects.filter(name=name).first()
            if user and check_password(password, user.password):
                request.session['user'] = user.to_dict()
                return redirect(reverse('blog:index'))
            else:
                login_form.add_error(forms.NON_FIELD_ERRORS, '用户名或密码错误')
        return render(request, 'login.html', {'form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            name = data.get('name')
            password = data.get('password')
            User.objects.create(name=name, password=make_password(password))
            return redirect(reverse('blog:index'))
        else:
            return render(request, 'register.html', {'form': register_form})


class LogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect(reverse('blog:login'))


class IndexView(View):
    @login_required
    def get(self, request, page=1):
        name = request.session['user']['name']
        from django.db.models import Count
        article_list = Article.objects.annotate(num=Count('articleread')).order_by('-comment_count', '-num')
        # article_list = Article.objects.all().order_by('-create_at', 'comment_set__count')
        paginator = Paginator(article_list, 10)
        article_list = paginator.get_page(page)
        # for article in article_list:
        # article.read_count = article.articleread_set.count()
        return render(request, 'index.html', {'article_list': article_list})


class PublishArticleView(View):
    def get(self, request):
        return render(request, 'publish_article.html')

    def post(self, request):
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.instance.user_id = request.session['user']['id']
            article_form.save()
            return redirect(reverse('blog:index'))
        return render(request, 'publish_article.html', {'form': article_form})


class ArticleDetailView(View):
    def get(self, request, id):
        # 添加文章阅读记录
        ArticleRead.objects.create(article_id=id, user_id=request.session['user']['id'])
        article = Article.objects.get(id=id)
        comment_list = article.comment_set.all()
        return render(request, 'article_detail.html', {'article': article, 'comment_list': comment_list})


class UserInformationView(View):
    def get(self, request, id):
        # id为空，默认为查看自己的信息
        if not id:
            id = request.session['user']['id']
        user = User.objects.get(id=id)
        article_list = Article.objects.filter(user_id=id).order_by('-create_at')
        is_followed = True if user.followed_user.filter(user_id=request.session['user']['id']) else False
        return render(request, 'user_information.html',
                      {'user': user, 'is_followed': is_followed, 'article_list': article_list})


class UserArticleManageView(View):
    def get(self, request):
        id = request.session['user']['id']
        user = User.objects.get(id=id)
        article_list = Article.objects.filter(user_id=id).order_by('-create_at')
        return render(request, 'user_article_manage.html', {'user': user,
                                                            'article_list': article_list})


class UserNoticeView(View):
    def get(self, request):
        user = User.objects.get(id=request.session['user']['id'])
        notice_type_list = NoticeType.objects.all()
        return render(request, 'user_notice.html', {'user': user, 'notice_type_list': notice_type_list})


class UserFollowView(View):
    @login_required
    def get(self, request):
        id = request.session['user']['id']
        user = User.objects.get(id=id)
        follow_users = User.objects.filter(followed_user__user_id=id)
        return render(request, 'user_follow.html', {'user': user,
                                                    'follow_users': follow_users})


class UserFollowedView(View):
    def get(self, request):
        id = request.session['user']['id']
        user = User.objects.get(id=id)
        followed_users = User.objects.filter(follow_user__follow_user_id=id)
        follow_users = User.objects.filter(followed_user__user_id=id).filter(
            followed_user__follow_user__in=followed_users)
        return render(request, 'user_followed.html', {'user': user,
                                                      'followed_users': followed_users,
                                                      'follow_users': follow_users})


class PublishCommentView(View):
    def post(self, request, article_id):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.article_id = article_id
            comment_form.instance.user_id = request.session['user']['id']
            comment_form.save()
            # 文章的评论数+1
            Article.objects.filter(id=article_id).update(comment_count=F('comment_count') + 1)
            # 创建评论通知
            article = Article.objects.get(id=article_id)
            article_title = article.title
            if len(article_title) > 10:
                article_title = article_title[:7] + '...'
            comment_content = comment_form.instance.content
            if len(comment_content) > 10:
                comment_content = comment_content[:7] + '...'
            context = {
                'article_id': article.id,
                'article_title': article_title,
                'comment_id': comment_form.instance.id,
                'comment_content': comment_content
            }
            Notice.objects.create(sender_id=request.session['user']['id'], receiver_id=article.user.id,
                                  type=NoticeType.objects.get(name=NoticeType.COMMENT_NOTICE),
                                  context=json.dumps(context))
        return HttpResponseRedirect(reverse('blog:article_detail', kwargs={'id': article_id}))


class ModifyUserInfoView(View):
    def get(self, request):
        user = User.objects.get(id=request.session['user']['id'])
        return render(request, 'modify_user_info.html', {'user': user})

    def post(self, request):
        user = User.objects.get(id=request.session['user']['id'])
        modify_user_info_form = ModifyUserInfoForm(request.POST, instance=user)
        if modify_user_info_form.is_valid():
            modify_user_info_form.instance.save()
        return render(request, 'modify_user_info.html', {'user': user})


class ProfilePictureListView(View):
    def get(self, request):
        profile_picture_list = ProfilePicture.objects.filter(is_system=True)
        return render(request, 'profile_picture_list.html', {'profile_picture_list': profile_picture_list})


class ModifyProfilePictureView(View):
    def get(self, request, id):
        User.objects.filter(id=request.session['user']['id']).update(profile_picture_id=id)
        return redirect(reverse('blog:modify_user_info'))


class NoticeListView(View):
    def get(self, request, notice_type_id):
        notice_type = NoticeType.objects.get(id=notice_type_id)
        notice_list = Notice.objects.filter(type_id=notice_type_id)
        template = Template(notice_type.template)
        for notice in notice_list:
            notice.context = json.loads(notice.context)
            ctx = Context(notice.context)
            notice.content = template.render(ctx)
        return render(request, 'notice_list.html', {'NoticeType': NoticeType, 'notice_list': notice_list})


def ajax_follow(request, user_id):
    Follow.objects.create(user_id=request.session['user']['id'], follow_user_id=user_id)
    return HttpResponse('true')


def ajax_cancel_follow(request, user_id):
    print('cancel', user_id)
    Follow.objects.filter(user_id=request.session['user']['id'], follow_user_id=user_id).delete()
    return HttpResponse('true')


@csrf_exempt
def ajax_reply(request, comment_id):
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        reply_form.instance.comment_id = comment_id
        reply_form.instance.user_id = request.session['user']['id']
        reply_form.save()
        # 文章的评论数+1
        comment = Comment.objects.get(id=comment_id)
        Article.objects.filter(id=comment.article_id).update(comment_count=F('comment_count') + 1)
        # 创建回复通知
        article = Article.objects.get(id=comment.article_id)
        article_title = article.title
        if len(article_title) > 10:
            article_title = article_title[:7] + '...'
        comment_content = comment.content
        if len(comment_content) > 10:
            comment_content = comment_content[:7] + '...'
        reply_content = reply_form.instance.content
        if len(reply_content) > 10:
            reply_content = reply_content[:7] + '...'
        context = {
            'article_id': article.id,
            'article_title': article_title,
            'comment_id': comment.id,
            'comment_content': comment_content,
            'reply_content': reply_content
        }
        Notice.objects.create(sender_id=request.session['user']['id'], receiver_id=article.user.id,
                              type=NoticeType.objects.get(name=NoticeType.REPLY_NOTICE),
                              context=json.dumps(context))
    return HttpResponse('true')
