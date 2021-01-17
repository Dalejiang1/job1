from django.test import TestCase

# Create your tests here.
# QQ登录接口1
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import json

from meiduo_mall.utils.secret import SecretOauth

from QQLoginTool.QQtool import OAuthQQ
from oauth.models import OAuthQQUser


class QQURLView(View):
    def get(self, request):
        next = request.GET.get('next')

        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next
        )
        login_url = oauth.get_qq_url()

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'login_url': login_url
        })


# QQ登录接口2
class QQUserView(View):

    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            return JsonResponse()
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state='/'

        )
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            print(e)
            return JsonResponse({})
        # TODO:判断用户是否绑定账号
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            # 未绑定 —— 加密openid返回给前端(前端跳转到绑定页面)
            access_token = SecrectOauth().dump({'openid': openid})
            return JsonResponse({'code': 400, 'errmsg': 'ok', 'access_token': access_token})
        else:
            # 已经绑定 —— 直接正常响应 —— 登陆成功

            user = oauth_user.user
            login(request, user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})

            response.set_cookie('username', user.username, max_age=14 * 3600 * 24)
            return response

    # qq登录接口3
    def post(self, request):
        data = json.loads(request.body.decode())
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')

        if not all({}):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
