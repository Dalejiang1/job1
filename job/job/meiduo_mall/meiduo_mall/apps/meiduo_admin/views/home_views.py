

#用于统计总数


from django.utils import timezone


from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


from users.models import User
from orders.models import OrderInfo


class UserTotalCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        #1 用于统计注册用户的总数量

        count=User.objects.count()
        #当前时刻

        cur_time=timezone.localtime()
        print('cur_time:',cur_time)



        return Response({

            'count':count,
            'date':cur_time.date()
        })

#日增加用户
#需求分析 此刻的时间大于0点的时间,模型类过滤统计

class DayIncreaseCountView(APIView):

    permission_classes = [IsAdminUser]

    def get(self,request):
        #当前时间
        cur_time=timezone.localtime()
        #0点时间
        cur_0_time=cur_time.replace(hour=0,minute=0,second=0)

        count=User.objects.filter(
            date_joined__gte= cur_0_time
        ).count()

        return Response({
            'count':count,
            'date':cur_0_time.date()
        })

#日活跃用户统计
#需求分析 上次登录时间大于当日0点的时间,模型类过滤

class DayActiveCountView(APIView):


    permission_classes = [IsAdminUser]

    def get(self,request):

        cur_time=timezone.localtime()

        cur_0_time=cur_time.replace(hour=0,minute=0,second=0)

        count=User.objects.filter(
            last_login__gte=cur_0_time
        ).count()

        #返回响应
        return  Response({
            'count':count,
            'date':cur_0_time.date()

        })

#日下单用户量统计
#需求分析 #1已知条件，订单从表找主表用户
#2 主表关联从表order


class UserOrderCountView(APIView):

# #(1)从从表入手查询
#     permission_classes = [IsAdminUser]
#     def get(self,request):
#
#
#         cur_time=timezone.localtime()
#         cur_0_time=cur_time.replace(hour=0,minute=0,second=0)
#
#
#         orders=OrderInfo.objects.filter(
#             create_time__gte=cur_0_time
#         )
#         user_set=set()
#
#         for order in orders:
#             user_set.add(order)
#
#         count=len(user_set)
#         return Response({
#             'count':count,
#             'date':cur_0_time
#         })
#（2）从主表入手

    permission_classes = [IsAdminUser]

    def get(self,request):

        cur_time=timezone.localtime()
        cur_0_time=cur_time.replace(hour=0,minute=0,second=0)

        users = User.objects.filter(orders__create_time__gte=cur_0_time)
        #去重
        count=len(set(users))

        return Response({
            'count':count,
            'date':cur_0_time
        })

#月新增用户
#需求分析

from datetime import timedelta

class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        # 1、获取当日的0时刻
        cur_time = timezone.localtime()
        # 当日0时刻(也是30天中最后一天的0时刻)：2021-1-8 0:0:0 +8:00
        end_0_time = cur_time.replace(hour=0, minute=0, second=0)
        # 2、起始日期的0时刻
        # start_0_time =  end_0_time  -  (统计天数 - 1)
        start_0_time = end_0_time - timedelta(days=29)

        data=[]
        for index in range(30):
            #其中某一天用于计算0时刻
            calc_0_time=start_0_time+timedelta(days=index)
            #次日的0时刻
            next_0_time=calc_0_time+timedelta(days=1)

            count=User.objects.filter(
                date_joined__gte=calc_0_time,
                date_joined__lt=next_0_time
            ).count()

            data.append({
                'count':count,
                'date':calc_0_time
            })
            return Response(data)

#分类访问量统计
from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.home_serializers import *
# 分类访问量统计
class GoodsDayView(ListAPIView):
    queryset = GoodsVisitCount.objects.all()
    serializer_class = GoodsVisitCountModelSerializer

    def get_queryset(self):
        # 获取当日0时刻
        cur_0_time = timezone.localtime().replace(hour=0, minute=0, second=0)
        # 对类属性queryset查询集进一步过滤
        return self.queryset.filter(create_time__gte=cur_0_time)





















