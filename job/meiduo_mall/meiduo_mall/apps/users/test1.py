# #判断用户名重复接口
# from django.contrib.auth.models import User
# from django.views import View
# from django.http import JsonResponse
#
#
# class UsernameCountView(View):
#
#     def get(self,request,username):
#
#         try:
#             count=User.objects.filter(username=username).count()
#         except Exception as e:
#             return JsonResponse({'code':400,'errmsg':'访问数据库失败'})
#         return JsonResponse({'code':0,'errmsg':'ok','count':count})


#浏览记录

# class UerBrowseHistory(View):
#
#     def post(self,request):
#         json_dict=json.loads(request.body.decode())
#
#         sku_id=json_dict.get('sku_id')
#
#         try:
#             SKU.objects.get(id=sku_id)
#         except SKU.DoesNotExist:
#             return JsonResponse('sku不存在')
#
#         #保存用户浏览数据
#         redis_conn=get_redis_connection('history')
#         p1=redis_conn.pipeline()
#         save_key='history_%s'%request.user.id
#
#         p1.lrem(save_key,0,sku_id)
#         p1.lpush(save_key,sku_id)
#         p1.ltrim(save_key,0,4)
#         p1.execute()
#
#         return JsonResponse({'code':0,'errmsg':'ok'})
#
# class UserBrowseHistory(View):
#     def get(self,request):
#         redis_conn=get_redis_connection('history')
#         sku_ids=redis_conn.lrange('history_%s'%request.user.id,0,-1)
#         #根据sku_ids列表数据，查询出商品sku信息
#
#         skus=[]
#         for sku_id in sku_ids:
#             sku=SKU.objects.get(id=sku_id)
#             skus.append({
#                 'id':sku_id,
#                 'name':sku.name,
#                 'default_image_url':sku.default_image,
#                 'price':sku.price
#
#
#             })
#
#             return JsonResponse({
#                 'code':0,
#                 'errmsg':'ok',
#                 'skus':skus
#             })
