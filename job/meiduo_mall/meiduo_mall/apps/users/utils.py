# 导入:
from django.contrib.auth.backends import ModelBackend
import re
from .models import User
from meiduo_mall.utils.secret import SecretOauth
from django.conf import settings


def get_user_by_account(account):
    '''判断 account 是否是手机号, 返回 user 对象'''
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # account 是手机号
            # 根据手机号从数据库获取 user 对象返回.
            user = User.objects.get(mobile=account)
        else:
            # account 是用户名
            # 根据用户名从数据库获取 user 对象返回.
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        # 如果 account 既不是用户名也不是手机号
        # 我们返回 None
        return None
    else:
        # 如果得到 user, 则返回 user
        return user

# 继承自 ModelBackend, 重写 authenticate 函数
class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法，实现用户名和mobile登录功能
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return: user
        """

        # 自定义验证用户是否存在的函数:
        # 根据传入的 username 获取 user 对象
        # username 可以是手机号也可以是账号
        user = get_user_by_account(username)

        # 校验 user 是否存在并校验密码是否正确
        if user and user.check_password(password):
            # 如果user存在, 密码正确, 则返回 user
            return user
#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
#
#
#
class LoginRequiredJSONMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        # 默认该函数返回的是一个重定向响应对象HttpResponseRedirect
        # 我们为了和美多商城工程一致，需要返回一个JsonResponse
        return JsonResponse({'code': 400, 'errmsg': '未登陆'})

    # 构造验证链接verify_url
def generate_verify_email_url(request):
    """
    功能: 加密用户数据成token，拼接完成的验证链接verify_url返回
    参数：request请求对象 —— 通过请求对象获取user用户对象
    返回值：完整的验证链接
    """
    # 加密获取token值
    token = SecretOauth().dumps({
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })
    # 拼接完整验证链接
    verify_url = settings.EMAIL_VERIFY_URL + token

    return verify_url