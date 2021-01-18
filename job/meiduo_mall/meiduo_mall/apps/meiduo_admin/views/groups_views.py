"""
分组管理视图
"""
from django.contrib.auth.models import Permission, Group
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.groups_serializers import *
from meiduo_admin.paginations import MyPage

class GroupPermListView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermSimpleModelSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = MyPage