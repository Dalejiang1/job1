from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.perm_serializers import *
from meiduo_admin.paginations import MyPage

class ContentTypeListView(ListAPIView):
    queryset=ContentType.objects.all()
    serializer_class = ContentModelSerializer

class PermViewSet(ModelViewSet):

    queryset = Permission.objects.all()
    pagination_class = MyPage

    serializer_class = PermModelSerializer

    def get_queryset(self):
        return self.queryset.order_by('pk')







