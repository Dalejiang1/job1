"""
定义关于SPU管理中的序列化器
"""
from rest_framework import serializers

from goods.models import SPU,Brand,GoodsCategory


#SPU序列化器
class SPUGoodsModelSerializer(serializers.ModelSerializer):

    brand_id=serializers.IntegerField()
    brand=serializers.StringRelatedField(read_only=True)
    category1_id=serializers.IntegerField()
    category2_id=serializers.IntegerField()
    category3_id=serializers.IntegerField()




    class Meta:
        model=SPU
        exclude = ('category1', 'category2', 'category3')


#Brand序列化器

class BrandModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Brand
        fields=[
            "id",
            "name"
        ]

#SPU分级序列化器

class GoodsCateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=GoodsCategory
        fields=[
            "id",
            "name"
        ]