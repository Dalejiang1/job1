from django.contrib.auth.models import Permission,ContentType
from rest_framework import serializers

class ContentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields=[
            "id",
            "name"
        ]




class PermModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Permission
        fields=[
            "id",
            "name",
            "codename",
            "content_type"
        ]

