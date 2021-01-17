# from django.db import models
#
# # Create your models here.
# from meiduo_mall.utils.models import BaseModel
#
#
# class Payment(BaseModel):
#     order=models.ForeignKey(orderInfo,on_delete=models.CASCADE,verbose_name='订单')
#     trade_id=models.CharField(max_length=100,unique=True,null=True,blank=True,verbose_name='支付编号')
#
#     class Meta:
#         db_table='tb_payment'
