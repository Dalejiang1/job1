from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers import option_serializers
from goods.models import SpecificationOption
from meiduo_admin.serializers.option_serializers import SpecOptModelSerializer
from meiduo_admin.paginations import MyPage

class OptionViewSet(ModelViewSet):

    queryset = SpecificationOption.objects.all()
    serializer_class = SpecOptModelSerializer

    pagination_class = MyPage
class SpecSimpleListView(ListAPIView):
    queryset = SpecificationOption.objects.all()
    serializer_class = SpecOptModelSerializer




