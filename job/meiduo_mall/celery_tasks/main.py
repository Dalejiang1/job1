"""
使用celery搭建一步程序，学习使用该程序来实现"异步发送短信"
# 安装到虚拟环境, 你懂得~
pip install Celery -i https://pypi.tuna.tsinghua.edu.cn/simple

# main.py文件，是我们异步程序的主脚本文件(相当于django中的manage.py)
"""
# TODO: 在celery运行指出，首先加载django配置环境
import os,django
# (1)、执行配置文件导包路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE','meiduo_mall.settings.dev')

django.setup()


from celery import Celery



celery_app = Celery('meiduo')

celery_app.config_from_object('celery_tasks.config')

#自动捕获tasks
celery_app.autodiscover_tasks([
    'celery_tasks.sms',
    'celery_tasks.email',
])

