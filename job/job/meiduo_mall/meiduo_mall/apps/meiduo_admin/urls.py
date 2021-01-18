from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views.home_views import *
from meiduo_admin.views.user_views import *
from meiduo_admin.views.sku_views import *
from meiduo_admin.views.spu_views import *
from meiduo_admin.views.spec_views import *
from meiduo_admin.views.option_views import *
from meiduo_admin.views.images_views import *
from meiduo_admin.views.order_views import *
from meiduo_admin.views.perm_views import *
from meiduo_admin.views.groups_views import *

urlpatterns=[

    path('authorizations/',obtain_jwt_token),

    # 用户总数统计
    path('statistical/total_count/', UserTotalCountView.as_view()),
    #日增用户数
    path('statistical/day_increment/',DayIncreaseCountView.as_view()),
    path('statistical/day_active/',DayActiveCountView.as_view()),
    path('statistical/day_orders/',UserOrderCountView.as_view()),
    path('statistical/month_increment/',UserMonthCountView.as_view()),
    path('statistical/goods_day_views/',GoodsDayView.as_view()),
    path('users/',UserView.as_view()),

        # SKU列表数据和单一新建
    path('skus/', SKUGoodsView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    # SKU单一数据
    path('skus/<int:pk>/', SKUGoodsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    # 新建SKU可选三级分类列表数据
    path('skus/categories/', SKUGoodsCateView.as_view()),
    # 新建SKU可选SPU列表数据
    path('goods/simple/', SPUSimpleView.as_view()),
    # 新建SKU用户选择的SPU所关联的规格和选项信息
    path('goods/<int:pk>/specs/', SpecOptView.as_view()),

    #SPU列表数据和单一新建
    path('goods/',SPUGoodsView.as_view({

        'get': 'list',
        'post':'create'
    })),

    #SPU品牌信息
    path('goods/brands/simple/',BrandSimpleListView.as_view()),

    # 新建SPU可选一级分类
    path('goods/channel/categories/', CateSimpleListView.as_view()),
    # 新建SPU可选二三级分类
    path('goods/channel/categories/<int:pk>/', CateSimpleListView.as_view()),

    #SPU单一数据
    path('goods/<int:pk>/',SPUGoodsView.as_view({
        "get":"retrieve",
        "put":"update",
        "delete":"destroy"
    })),

    #SPU规格列表数据
    path('goods/specs/',SPUSpecView.as_view({
        "get":"list",
        "post":"create"
    })),
    #获取单一规格
    path('goods/specs/<int:pk>/',SPUSpecView.as_view({
        'get': 'retrieve',
        "post":"update",
        "delete":"destroy"
    })),

    # 选项表管理
    path('specs/options/', OptionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('specs/options/<int:pk>/', OptionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新建选项可选规格
    path('goods/specs/simple/', SpecSimpleListView.as_view()),
    # 图片管理
    path('skus/images/', ImageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('skus/images/<int:pk>/', ImageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    # 新建图片可选sku
    path('skus/simple/', ImageViewSet.as_view({
        'get': 'simple'
    })),

    #订单列表
    path('orders/',OrderView.as_view({
        'get':'list',
    })),

    #订单详情列表
    path('orders/<str:pk>/',OrderView.as_view({
        "get":"retrieve",
    })),
    path('orders/<str:pk>/status/', OrderView.as_view({
        'patch': 'partial_update'
    })),

    # 权限管理
    path('permission/perms/', PermViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('permission/perms/<int:pk>/', PermViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新增权限可选类型
    path('permission/content_types/', ContentTypeListView.as_view()),
    # 分组管理
    path('permission/groups/', GroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('permission/groups/<int:pk>/', GroupViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
# 新建分组可选权限
    path('permission/simple/', GroupPermListView.as_view()),
]