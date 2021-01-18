# from django.shortcuts import render
# from django.views import View
# from django.http import JsonResponse
# from django.contrib.auth import login
# from django_redis import get_redis_connection
# import json,re
# from QQLoginTool.QQtool import OAuthQQ
# from oauth.models import OAuthQQUser
# from users.models import User
#
# #QQ登录接口1
#
# class QQURLView(View):
#     def get(self,resquest):
#
#         next=request.GET.get('next')
#         oauth=OAuthQQ(
#             client_id=setting.QQ_CLINT_ID,
#             client_secret=setting.QQ_CLINT_SECRET,
#             redirect_url=setting.QQ_REDIRECT_URL,
#             start=next
#
#
#         )
#         login_url=oauth.get_qq_url()
#
#         return JsonResponse({
#             'code':0,
#             'errmsg':'ok',
#             'login_url':login_url
#
#         })
# #编辑oauth/urld.py 映射路由
#
# path('qq/authorization/',views.QQURLView.as_view()),
#

