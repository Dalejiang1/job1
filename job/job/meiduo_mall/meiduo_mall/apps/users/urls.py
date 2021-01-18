from django.urls import path,re_path

from . import views

urlpatterns=[
    # path('user/',views.),
    # re_path('^/usernames/(?P<username>[a-zA-Z0-9_-]{5,20})$/count/',views.UsernameCountView.as_view()),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.MobileCountView.as_view()),
    path('register/',views.RegisterView.as_view()),
    #传统登录
    path('login/',views.LoginView.as_view()),
    # 退出登陆
    path('logout/', views.LogoutView.as_view()),
    path('info/',views.UserInfoView.as_view()),
    # 添加邮箱
    path('emails/', views.EmailView.as_view()),
    # 新增用户地址
    path('addresses/create/', views.CreateAddressView.as_view()),
    # 展示用户地址
    path('addresses/', views.AddressView.as_view()),
    # 更新和删除地址
    path('addresses/<int:address_id>/', views.UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    path('addresses/<int:address_id>/default/', views.DefaultAddressView.as_view()),
    # 设置地址标题
    path('addresses/<int:address_id>/title/', views.UpdateTitleAddressView.as_view()),
    # 修改密码
    path('password/', views.ChangePasswordView.as_view()),


    #用户浏览记录
    path('browse_histories/',views.UserBrowseHistory.as_view()),
]