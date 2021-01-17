from rest_framework.generics import ListAPIView
from rest_framework.serializers import *
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.paginations import MyPage
from goods.models import SPU, SPUSpecification, SpecificationOption, Brand,GoodsCategory,GoodsChannelGroup,GoodsChannel
from meiduo_admin.serializers.spu_serializers import SPUGoodsModelSerializer, BrandModelSerializer,GoodsCateModelSerializer

class SPUGoodsView(ModelViewSet):
    """
        SPU表的增删改查
    """
    # 指定序列化器
    serializer_class = SPUGoodsModelSerializer
    # 指定查询及
    queryset = SPU.objects.all()
    # 指定分页
    pagination_class = MyPage
    def get_queryset(self):
        keyword=self.request.query_params.get("keyword")
        if keyword:
            return self.queryset.filter(
                name__contains=keyword
            )
        return self.queryset.all()



#SPU品牌表

class BrandSimpleListView(ListAPIView):
    serializer_class = BrandModelSerializer
    queryset = Brand.objects.all()



#SPU分级分类
class CateSimpleListView(ListAPIView):
    serializer_class = GoodsCateModelSerializer
    queryset = GoodsCategory.objects.all()
    def get_queryset(self):
        parent_id=self.kwargs.get('pk')

        if parent_id:
            return self.queryset.filter(parent_id=parent_id)
        else:
            return self.queryset.filter(parent=None)





