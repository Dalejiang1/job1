from rest_framework import serializers

from goods.models import SpecificationOption

class SpecOptModelSerializer(serializers.ModelSerializer):
    spec=serializers.StringRelatedField()

    class Meta:
        model=SpecificationOption
        fields="__all__"