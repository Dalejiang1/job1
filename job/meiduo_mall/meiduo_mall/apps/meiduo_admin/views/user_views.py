from rest_framework.generics import ListAPIView,CreateAPIView
from meiduo_admin.serializers.user_serializers import *
from meiduo_admin.paginations import MyPage

class UserView(ListAPIView,CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    pagination_class = MyPage#指定分页器

    def get_queryset(self):

        key_word=self.request.query_params.get('keyword')

        #过滤
        if key_word:
            return self.queryset.filter(username_contains=key_word)
        else:
            return self.queryset.all()
