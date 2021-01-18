from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.spec_serializers import *
from meiduo_admin.paginations import MyPage


class SPUSpecView(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SPUSpecModelSerializer

    pagination_class = MyPage




