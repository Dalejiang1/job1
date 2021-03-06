"""
自定义文件存储后端，实现拼接完整图片链接
所谓的Django存储后端，决定了我们文件类型字段的新建保存和访问。
"""
# Storage是Django默认的存储后端
from django.core.files.storage import Storage
from django.conf import settings
#
from fdfs_client.client import Fdfs_client
from rest_framework.exceptions import ValidationError



class FastDFSStorage(Storage):

    def __init__(self, fdfs_base_url=None):
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        # 功能：打开django本地文件
        pass

    def _save(self, name, content, max_length=None):
        # 功能：保存文件 —— 项目二实现
        #提取文件数据
        data=content.read()

        conn=Fdfs_client(settings.FDFS_PATH)
        res=conn.upload_appender_by_buffer(data)

        if res['Status'] !='Upload successed.':
            raise ValidationError('fdfs上传失败')
        file_id=res['Remote file_id']

        return file_id

    def exists(self, name):


        return False




    def url(self, name):
        # 功能：拼接返回完整的图片链接
        # 参数：name是文件索引标识(存储在mysql中文件id)
        return self.fdfs_base_url + name
