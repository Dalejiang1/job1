"""
定义首页index.html静态化函数
django就是根据MVT模型设计的
M —— model模型类，操作数据库
V —— View视图，编写业务代码视图函数，用于响应请求
T —— Template模版，渲染静态页面
"""
from django.template import loader
from django.conf import settings
import os

from .utils import get_categories
from .models import Content,ContentCategory

# 美多商城首页index.html的静态化函数
def generate_static_index_html():
    # 1、构建模版参数
    catgories = get_categories() # 获取首页频道分类导航信息模版参数
    contents = {} # 获取首页广告模版参数

    # 读取所有广告分类——广告位置
    content_categories = ContentCategory.objects.all()
    for content_cat in content_categories:
        # contents['index_lbt'] = [广告对象1， 广告对象2....]
        contents[content_cat.key] = Content.objects.filter(
            category=content_cat,
            status=True
        ).order_by('sequence')

    context = {
        'categories': catgories,
        'contents': contents
    }
    # 2、获取模版对象
    template = loader.get_template('index.html')
    # 3、渲染页面
    html = template.render(context=context)

    static_html_dir = os.path.join(os.path.dirname(os.path.dirname(settings.BASE_DIR)), 'front_end_pc')
    # 4、保存静态文件
    with open(os.path.join(static_html_dir, 'index.html'), 'w') as f:
        f.write(html)




# 编写一个测试案例函数，来讲解django的模版渲染接口
# 渲染一个完整的html静态页面
def demo_static():

    # 1、构建模版参数 —— 可能是数据库读取的
    # django的模版参数，支持类型：int、str等基础类型，以及列表元组，字典等。还支持模型类对象。
    context = {
        'book_list': [
            {'btitle': '射雕英雄传', 'bpub_date': '1999-9-6'},
            {'btitle': '雪山飞狐', 'bpub_date': '1976-12-6'},
            {'btitle': '水浒传', 'bpub_date': '1998-9-4'}
        ]
    }
    # 2、获取模版对象 —— 加载html模版
    template = loader.get_template('demo.html')
    # 3、渲染页面 —— 静态化，把动态模版参数填充到html模版中
    html = template.render(context=context)

    # 4、把html完整的页面数据保存成静态文件
    with open('/Users/weiwei/Desktop/meiduo_mall_sz41/front_end_pc/demo.html', 'w') as f:
        f.write(html)
