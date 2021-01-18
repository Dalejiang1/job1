from rest_framework import serializers
from goods.models import GoodsVisitCount

class GoodsVisitCountModelSerializer(serializers.ModelSerializer):

    category=serializers.StringRelatedField()

    class Meta:
        model=GoodsVisitCount
        fields=['category','count']
