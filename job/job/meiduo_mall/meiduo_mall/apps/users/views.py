# from django.shortcuts import render
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# #
# # # Create your views here.
# from django import http
# from django.views import View
#
#
# # 注意User的导包路径
# from users.models import User


from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from django_redis import get_redis_connection
import json,re

from goods.models import SKU
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from users.models import User
from users.utils import generate_verify_email_url
from celery_tasks.email.tasks import send_verify_email


import logging
logger = logging.getLogger('django')
# Create your views here.


# import logging
# logger = logging.getLogger('django')

class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        '''判断用户名是否重复'''
        # 1.查询username在数据库中的个数
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400, 'errmsg':'访问数据库失败'})

        # 2.返回结果(json) ---> code & errmsg & count
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count':count})

class MobileCountView(View):

    def get(self, request, mobile):
        '''判断手机号是否重复注册'''
        # 1.查询mobile在mysql中的个数
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400, 'errmsg':'查询数据库出错'})

        # 2.返回结果(json)
        return JsonResponse({'code':0, 'errmsg':'ok', 'count':count})





from django.http import JsonResponse
import json
import re

class RegisterView(View):

    def post(self, request):
        # 1、提取参数
        # request.body --> b"{'username': 'weiwei'....}"
        json_str = request.body.decode() # "{'username': 'weiwei'....}"
        data = json.loads(json_str) # {'username': 'weiwei'....}

        # 必传
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        sms_code = data.get('sms_code')
        # 非必传
        allow = data.get('allow', False)

        # 2、校验参数
        # 2.1、必要性校验
        # 当且仅当username、password、password2、mobile和sms_code都不为None，表示都传了
        if not all([username, password, password2, mobile, sms_code]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必要参数'
            })

        # 2.2、约束性校验
        if not allow:
            return JsonResponse({
                'code': 400,
                'errmsg': '请勾选同意用户协议'
            })
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({
                'code': 400,
                'errmsg': '用户名格式有误'
            })
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '手机号格式有误'
            })
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码格式有误'
            })
        if password != password2:
            return JsonResponse({
                'code': 400,
                'errmsg': '密码输入不一致'
            })

        # 2.3、业务性校验 —— 短信验证码等。
        # TODO: 此处将来填充校验短信验证码逻辑代码

        # 3、业务数据处理 —— 新建用户模型类对象保存数据库，用户状态保持。
        try:
            # User.objects.create() --> 密码未加密
            # User.objects.create_user() --> 密码加密。AbstractUser提供都方法
            # User.objects.create_superuser() --> 密码加密,超级管理员。要求必传email。AbstractUser提供都方法
            # 此处项目一新建的是普通用户，所以只需使用create_user
            user = User.objects.create_user(
                username=username,
                password=password,
                mobile=mobile
            )
        except Exception as e:
            print(e)
            logger.error('注册用户，写入mysql失败！')
            return JsonResponse({
                'code': 400,
                'errmsg': '服务器繁忙，请稍后。'
            })

        # TODO: 用户状态保持 —— 把用户数据写入session，用于下一次请求验证用户身份。

        # 4、构建响应
        response=JsonResponse({
            'code': 0,
            'errmsg': '恭喜，注册成功。'
        })
        # TODO: 在cookie中设置username记录登陆用户名作前端页面展示
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response


import json
from django.contrib.auth import login,authenticate

#用户登录
class LoginView(View):

    def post(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered', False)

        # 2、校验参数
        # 2.1、必要性校验
        if not all([username, password]):
            return JsonResponse({'code':400, 'errmsg': '缺少必要参数'})
        # 2.2、约束性校验
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({
                'code': 400,
                'errmsg': '用户名格式有误'
            })
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码格式有误'
            })

        # 3、业务处理(2.3、业务性校验) —— 根据用户填写的"用户名"和密码校验
        # 全局认证函数authenticate
        # 功能：根据username和password校验用户 —— 只支持用户名校验(不支持多账号)
        # 参数：用户名username和密码password
        # 返回值：校验成功返回用户对象，如果校验失败None
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})

        # TODO: 状态保持
        login(request, user)

        # TODO: 判断是否记住用户信息
        if remembered:
            # 用户勾选了，长期状态保持
            request.session.set_expiry(None) # 如果这是为None。表示该用户session数据记录2周有效期
        else:
            # 用户没勾选，短期状态保持 —— 用户关闭浏览器页面后失效
            request.session.set_expiry(0) # 设置为0表示立即失效 —— 关闭浏览器在请求则session用户数据失效

        # 4、构建响应
        response=JsonResponse({'code': 0,'errmsg': 'ok'})
        # TODO: 在cookie中设置username记录登陆用户名作前端页面展示
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response

#
# 导入:
from django.contrib.auth import logout

class LogoutView(View):
    """定义退出登录的接口"""

    def delete(self, request):
        """实现退出登录逻辑"""

        # 清理 session
        logout(request)

        # 创建 response 对象.
        response = JsonResponse({'code':0, 'errmsg':'ok'})

        # 调用对象的 delete_cookie 方法, 清除cookie
        response.delete_cookie('username')

        # 返回响应
        return response



from django.contrib.auth.mixins import LoginRequiredMixin
class UserInfoView(LoginRequiredMixin, View):
    # 视图函数
    def get(self, request):

        user = request.user

        # 已经登陆
        return JsonResponse({
            'code': '0',
            'errmsg': 'ok',
            'info_data': {
                'username': user.username,
                'mobile': user.mobile,
                'email': user.email,
                'email_active':True
                # 'email_active': user.email_active
            }
        })


class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 校验参数
        if not email:
            return JsonResponse({'code': 400,
                                      'errmsg': '缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400,
                                      'errmsg': '参数email有误'})


        # 赋值 email 字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400,
                                      'errmsg': '添加邮箱失败'})
        # TODO：发送验证邮件
        verify_url = generate_verify_email_url(request)
        send_verify_email.delay(email, verify_url)

        # 响应添加邮箱结果
        return JsonResponse({'code': 0,
                                  'errmsg': 'ok'})

from meiduo_mall.utils.secret import SecretOauth
# 激活邮箱 —— 验证token
class VerifyEmailView(View):
    def put(self, request):
        # 1、提取参数
        token = request.GET.get('token')
        # 2、校验参数
        if not token:
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        # 3、业务数据处理 —— 校验token有性，激活邮箱
        user_info = SecretOauth().loads(token)
        if user_info is None:
            return JsonResponse({'code': 400, 'errmsg': '邮箱验证失败'})
        user_id = user_info.get('user_id')
        email = user_info.get('email')
        try:
            user = User.objects.get(id=user_id, email=email, is_active=True)
        except User.DoesNotExist as e:
            logger.info('邮箱验证用户不存在或已注销：%s' % e)
            return JsonResponse({'code': 400, 'errmsg': '邮箱验证用户不存在或已经注销'})
        else:
            # 激活邮箱
            user.email_active = True
            user.save()
        # 4、构建响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

from .models import Address
#  新增用户收货地址
class CreateAddressView(LoginRequiredMixin, View):

    def post(self, request):
        # 1、提取参数
        json_dict = json.loads(request.body.decode())

        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 2、校验参数
        # 2.1、业务性校验 —— 收货地址不能超过20个
        user = request.user
        count = user.addresses.filter(is_deleted=False).count()
        if count >= 20:
            return JsonResponse({'code': 400, 'errmsg': '最多20个地址'})

        # 2.2、必要性校验
        if not all([
            receiver,
            province_id,
            city_id,
            district_id,
            place,
            mobile
        ]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        # 2.2、约束性校验
        if not re.match(r'^\w{1,20}$', receiver):
            return JsonResponse({'code': 400, 'errmsg': '收货人昵称有误'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})

        if tel:
            # if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
            if not re.match(r'\d{3}-\d{7,8}|\d{4}-\d{7,8}$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})

        # 3、业务数据处理  —— 新建Address对象保存数据库
        try:
            address = Address.objects.create(
                user = request.user,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                title=receiver, # 由于新增地址接口没有传递标题，此处默认把标题设置为receiver
                receiver=receiver,
                place=place,
                mobile=mobile,
                tel = tel or '', # tel if tel else ''
                email = email or ''
            )
            # 如果用户的default_address为空，把新增的收货地址设置为用户的默认收货地址
            user = request.user
            if not user.default_address:
                user.default_address = address
                user.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存收货地址错误'})

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'address': {
                'id': address.id,
                'title': address.title,
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email
            }
        })
# 展示收货地址 —— 把当前登陆用户的收货地址列表数据返回
class AddressView(LoginRequiredJSONMixin, View):

    def get(self, request):
        # 1、提取参数
        user = request.user
        # 2、校验参数
        # 3、业务数据处理 —— 地址返回
        addresses = user.addresses.filter(is_deleted=False)
        print('查询集:', addresses)
        # 构建响应参数
        address_list = []
        for address in addresses:
            # 事先组织数据，记录数据
            address_dict = {
                    'id': address.id,
                    'title': address.title,
                    'receiver': address.receiver,
                    'province': address.province.name,
                    'city': address.city.name,
                    'district': address.district.name,
                    'place': address.place,
                    'mobile': address.mobile,
                    'tel': address.tel,
                    'email': address.email
            }

            # if address.id == user.default_address.id:
            #     address_list.insert(0, address_dict)
            # else:
            address_list.append(address_dict)
        # default_id=request.user.default_address.id
        print('返回的列表:', address_list)
        # 4、构建响应
        print('---------------------------',  type(user), user)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'default_address_id': user.default_address_id,
            'addresses': address_list
        })


class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    def put(self,request,address_id):

        user=request


        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 2、校验参数
        # 2.1、业务性校验 —— 收货地址不能超过20个
        user = request.user
        count = user.addresses.filter(is_deleted=False).count()
        if count >= 20:
            return JsonResponse({'code': 400, 'errmsg': '最多20个地址'})

        # 2.2、必要性校验
        if not all([
            receiver,
            province_id,
            city_id,
            district_id,
            place,
            mobile
        ]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        # 2.2、约束性校验
        if not re.match(r'^\w{1,20}$', receiver):
            return JsonResponse({'code': 400, 'errmsg': '收货人昵称有误'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})

        # 3、业务数据处理
        json_dict.pop('province')
        json_dict.pop('city')
        json_dict.pop('district')
        Address.objects.filter(
            pk=address_id
        ).update(**json_dict)  # update(receiver="韦小宝".....)
        # update(city="长治市"), city市外键关联字段，必须被赋值为模型类对象.所以此处直接赋值字符串是错误的。

        # 4、构建响应
        address = Address.objects.get(pk=address_id)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'address': {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
        })

        # 删除 —— 逻辑删除

    def delete(self, request, address_id):
        user = request.user
        try:
            address = Address.objects.get(pk=address_id, is_deleted=False)
            address.is_deleted = True
            address.save()

            if address.id == user.default_address.id:
                # 如果当前删除的地址刚好是用户的默认地址，把默认地址设置为用户最新增加的地址
                addresses = Address.objects.filter(user=user, is_deleted=False).order_by('-update_time')  # 地址查询集 或 一个空集
                if addresses:
                    user.default_address = addresses[0]
                else:
                    user.default_address = None
                user.save()

        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '删除地址有误'})

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


# 设置默认地址
class DefaultAddressView(LoginRequiredJSONMixin, View):

    def put(self, request, address_id):
        user = request.user

        try:
            address = Address.objects.get(pk=address_id, is_deleted=False)
        except Address.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': '地址无效'})

        user.default_address = address
        user.save()

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


# 修改地址标题
class UpdateTitleAddressView(LoginRequiredJSONMixin, View):

    def put(self, request, address_id):
        data = json.loads(request.body.decode())
        title = data.get('title')
        if not title:
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match(r'^\w{1,20}$', title):
            return JsonResponse({'code': 400, 'errmsg': 'title格式有误'})

        try:
            address = Address.objects.get(pk=address_id, is_deleted=False)
        except Address.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': '地址无效'})

        address.title = title
        address.save()

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


# 修改密码
class ChangePasswordView(LoginRequiredJSONMixin, View):

    def put(self, request):
        data = json.loads(request.body.decode())
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password2 = data.get('new_password2')

        if not all([old_password, new_password, new_password2]):
            return JsonResponse({
                'code': 400, 'errmsg': '缺少必要参数'
            })

        user = request.user
        # 检查旧密码
        if not user.check_password(old_password):
            return JsonResponse({'code': 400, 'errmsg': '旧密码输入错误'})

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', new_password):
            return JsonResponse({'code': 400, 'errmsg': '新密码格式有误'})
        if new_password != new_password2:
            return JsonResponse({'code': 400, 'errmsg': '新密码2次输入不一致'})

        if new_password == old_password:
            return JsonResponse({'code': 400, 'errmsg': '新旧密码不能一致'})

        # 修改密码
        user.set_password(new_password)
        user.save()

        # 请求用户状态保持
        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')

        return response


from goods.models import SKU,GoodsVisitCount
from django.utils import timezone

class UserBrowseHistory(LoginRequiredJSONMixin, View):

    # 记录用户浏览历史
    def post(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        # 2、校验参数
        if not sku_id:
            return JsonResponse({'code': 400, 'errmsg': '缺少sku_id参数'})
        try:
            sku = SKU.objects.get(pk=sku_id, is_launched=True)
        except SKU.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': '商品无效'})

        # 3、业务数据处理 —— 写入redis记录历史信息
        user = request.user
        conn = get_redis_connection('history') # 3号
        p = conn.pipeline()
        # (1)、去重
        p.lrem('history_%s'%user.id, 0, sku_id) # 0表示删除所有相同sku_id
        # (2)、存redis浏览历史
        p.lpush('history_%s'%user.id, sku_id) # 列表左侧插入，保证左侧最新访问
        # (3)、截取
        p.ltrim('history_%s'%user.id, 0, 4) # [0, 4]表示截取5条数据
        p.execute()

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })

    # 查询用户浏览历史
    def get(self, request):
        # 1、提取参数
        user = request.user
        # 2、校验参数
        # 3、业务数据处理 —— 访问redis获取浏览历史，访问mysql获取详情
        conn = get_redis_connection('history')
        # (1)、访问redis获取浏览历史
        # sku_ids = [b'1', b'2', b'3']
        sku_ids = conn.lrange('history_%s'%user.id, 0, -1) # 从左到右
        print('sku_ids: ', sku_ids)
        # (2)、访问mysql获取详情构建响应数据
        skus = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(pk=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        #TODO:记录sku_id商品访问类别
        cur_0_time=timezone.localtime().replace(hour=0,minute=0,second=0)

        category=sku.category
        #如果对象存在累加，不存在则新建

        try:
            visit=GoodsVisitCount.objects.get(
                category=category,
                create_time__gte=cur_0_time
            )
        except GoodsVisitCount.DoesNotExist as e:
            visit=GoodsVisitCount.objects.create(
                category=category,
                count=1
            )
        else:
            visit.count +=1
            visit.save()



        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'skus': skus
        })
