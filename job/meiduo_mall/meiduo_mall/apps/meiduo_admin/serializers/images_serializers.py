
"""
图片管理序列化器
"""

from rest_framework import serializers
from goods.models import SKU,SKUImage
from fdfs_client.client import Fdfs_client

from django.conf import settings
from rest_framework.exceptions import ValidationError

#新建可选图片

class SKUSimpleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=SKU
        fields=[
            "id",
            "name"
        ]

class ImageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=SKUImage
        fields=[
            "id",
            "sku",
            "image"
        ]

    #在校验过程中介入 实现上传图片到fdfs业务

    # def validate(self, attrs):
    #     f=attrs.get('image')
    #
    #     data=f.read()
    #
    #     #上传图片
    #     conn=Fdfs_client(settings.FDFS_PATH)
    #     res=conn.upload_appender_by_buffer(data)
    #     if res['Status'] !='Upload successed.':
    #         raise ValidationError('fdfs上传失败')
    #     file_id=res['Remote file_id']
    #
    #     return attrs
    #在新建的过程中介入
    def create(self, validated_data):

        f=validated_data.get('image')
        data=f.read()

        conn=Fdfs_client(settings.FDFS_PATH)
        res=conn.upload_appender_by_buffer(data)

        if res['Status'] != 'Upload successed.':
            raise ValidationError('上传fdfs失败')
        file_id=res['Remote file_id']

        image=SKUImage.objects.create(
            sku=validated_data.get('sku'),
            image=file_id
        )

        return image