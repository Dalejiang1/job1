"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# from django.views import View

urlpatterns = [
    path('admin/', admin.site.urls),
    #haystack
    # path('search/',include('haystack.urls')),
    # 2.添加users的总路由. 注意导入include函数:
    path('', include('users.urls')),
    path(r'', include('verifications.urls')),
    path('', include('oauth.urls')),
    path('', include('areas.urls')),
    path('', include('goods.urls')),
    path('', include('cats.urls')),
    path('', include('orders.urls')),
    path('', include('payment.urls')),

    path('meiduo_admin/',include('meiduo_admin.urls'))
]