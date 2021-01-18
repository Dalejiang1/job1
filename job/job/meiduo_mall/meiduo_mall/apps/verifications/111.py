# # from django.shortcuts import render
# # from django.views import View
# # from django.http import HttpResponse
# # from django.redis import get_redis_connection
# # from verifications.libs.captcha.captcha import captcha

# # #1 图形验证接口
# #
# # class ImageCodeView(View):
# #     def get(self,request,uuid):
# #         #1 提取参数
# #         #2 校验参数
# #         #3 业务数据处理
# #         #3.1 调用captcha生成图片和验证码
# #         text,image = captcha.generate_captcha()
# #         print('验证码：',text)
# #         #3.2 把验证码写入redis
# #         conn = get_redis_connection('verify_code')
# #         conn.setex('img_%s'%uuid,300,text)
# #         #4 构建响应
# #         return HttpResponse(
# #             image,
# #             content_type='imge/jpeg'
# #
# #         )
# # # 设置总路由
# #
# # from django.urls import path,include
# #
# # urlpatterns=[
# #     path(r'',include('verifications.urls')),
# # ]
# # #设置子路由
# # from django.urls import path,include
# #
# # from . import views
# # urlpatterns=[
# #     path('image_codes/<uuid=uuid>/',views.ImageCodeView.as_view()),
# #
# # ]
# #
# # #2 短信验证码接口
# # from django.shortcuts import render
# # from django.views import View
# # from django.http import HttpResponse,JsonResponse
# # from django_redis import get_redis_connection
# #
# # import re,random
# # from verifications.libs.yuntongxun.ccp_sms import CCP
# #
# #
# # class SMSCodeView(View):
# #     def get(self,request,mobile):
# #         # 1.提取参数
# #         image_code = request.Get.get('image_code')
# #         image_code_id = request.Get.get('image_code_id')
# #
# #         # 2.校验参数
# #         #2.1 必要校验
# #         if not all([image_code,image_code_id]):
# #             return JsonResponse({
# #                 'code':400,
# #                 'errmsg':'缺少参数'
# #             })
# #             # 2.2、约束校验
# #         if not re.match(r'^[a-zA-Z0-9]{4}$', image_code):
# #             return JsonResponse({'code': 400, 'errmsg': '图形验证码格式有误'}, status=400)
# #         if not re.match(r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$', image_code_id):
# #             return JsonResponse({'code': 400, 'errmsg': 'uuid有误！'}, status=400)
# #         # 2.3、业务校验 —— 校验用户填写的图形验证码image_code和redis存储的是否一致
# #         conn = get_redis_connection('verify_code') #2号库
# #         image_code_from_redis =conn.get('img_%s' %image_code_id)
# #
# #         conn.delete('img_%s'%image_code_id)
# #         if not image_code_from_redis:
# #             #过期了
# #
# #             return JsonResponse({'code':400,'errmsg':'图形验证码失效'})
# #         if image_code.lower() != image_code_from_redis.decode().lower():
# #             return JsonResponse({'code': 400, 'errmsg': '验证码输入有误'})
# #
# #         #3.业务数据处理-发短信 redis存短信验证码
# #         sms_code = '%06d'%random.randrange(0,999999)
# #         ccp =CCP()
# #         ccp.send_template_sms(
# #             mobile,
# #             [sms_code,5],
# #             1
# #         )
# #
# #         conn.setex('sms_%s'%mobile,300,sms_code)
# #
# #
# #
# #         # 4.响应结果
# #         return JsonResponse({
# #             'code':0,
# #             'errmsg':'ok'
# #         })
# #
# #     #设置子路由
# # from django.urls import path,re_path
# # from . import views
# #
# # urlpatterns[
# #     re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9}/$',views.SMSCodeView.as_view()),
# # ]
# #
# #3 判断用户名是否重复
# from django.http import JsonResponse
# from users.models import User
# from django.views import View
#
#
# import logging
# logger = logging.getLogger('django')
# class UsernameCountView(View):
#
#     def get(self,request,username):
#         try:
#             count = User.objects.filter(username=username).count()
#         except Exception as e:
#             return JsonResponse({
#                 'code':400,
#                 'errmsg':'访问数据库失败'
#             })
#         return JsonResponse({
#             'code':0,
#             'errmsg':'ok',
#             'count':count
#         })
#     #判断手机是否重复注册
# class MobileCountView(View):
#     def get(self,request,mobile):
#         try:
#             count=User.objects.filter(mobile=mobile).count()
#         except Exception as e:
#             return JsonResponse({
#                 'code':400,
#                 'errmsg':'查询数据库出错'
#             })
#         return JsonResponse({
#             'code':0,
#             'errmsg':'ok',
#             'count':count
#         })
#
#  #设置子路由
#
#  from django.urls import path,re_path
# from . import views
#
# urlpatterns=[
#     re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCount.as_viw()),
# ]
#