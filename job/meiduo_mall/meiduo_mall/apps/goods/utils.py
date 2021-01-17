from django.template import loader
from django.conf import settings
import os
from .models import GoodsCategory,GoodsChannel,SKUSpecification,SKU,SPUSpecification,SpecificationOption
from copy import deepcopy



from .models import GoodsCategory


def get_breadcrumb(category_id):
    """
    获取导航数据
    :param category_id: 分类id
    :return: 字典
    """
    # 根据传入的分类的id，构建1，2，3级分类导航
    category = GoodsCategory.objects.get(pk=category_id)
    # (1)、如果传来的是一级分类
    if not category.parent:
        return {
            'cat1': category.name
        }
    # (2)、如果传来的是二级分类
    if not category.parent.parent:
        return {
            'cat1': category.parent.name,
            'cat2': category.name
        }
    # (3)、如果传来的是三级分类
    if not category.parent.parent.parent:
        return {
            'cat1': category.parent.parent.name,
            'cat2': category.parent.name,
            'cat3': category.name
        }


# 构造sku商品详情页模版参数 —— 构造sku商品的规格和选项信息
def get_goods_and_spec(sku_id):
    # 当前SKU商品
    sku = SKU.objects.get(pk=sku_id)

    # 记录当前sku的选项组合
    cur_sku_spec_options = SKUSpecification.objects.filter(sku=sku).order_by('spec_id')
    cur_sku_options = [] # [1,4,7]
    for temp in cur_sku_spec_options:
        # temp是SKUSpecification中间表对象
        cur_sku_options.append(temp.option_id)

    # spu对象(SPU商品)
    goods = sku.spu
    # 罗列出和当前sku同类的所有商品的选项和商品id的映射关系
    # {(1,4,7):1, (1,3,7):2}
    sku_options_mapping = {}
    skus = SKU.objects.filter(spu=goods)
    for temp_sku in skus:
        # temp_sku:每一个sku商品对象
        sku_spec_options = SKUSpecification.objects.filter(sku=temp_sku).order_by('spec_id')
        sku_options = []
        for temp in sku_spec_options:
            sku_options.append(temp.option_id) # [1,4,7]
        sku_options_mapping[tuple(sku_options)] = temp_sku.id # {(1,4,7):1}

    # specs当前页面需要渲染的所有规格
    specs = SPUSpecification.objects.filter(spu=goods).order_by('id')
    for index, spec in enumerate(specs):
        # spec每一个规格对象
        options = SpecificationOption.objects.filter(spec=spec)
        # 每一次选项规格的时候，准备一个当前sku的选项组合列表，便于后续使用
        temp_list = deepcopy(cur_sku_options) # [1,4,7]

        for option in options:
            # 每一个选项，动态添加一个sku_id值，来确定这个选项是否属于当前sku商品
            temp_list[index] = option.id # [1,3,7] --> sku_id?
            option.sku_id = sku_options_mapping.get(tuple(temp_list)) # 找到对应选项组合的sku_id

        # 在每一个规格对象中动态添加一个属性spec_options来记录当前规格有哪些选项
        spec.spec_options = options

    # goods是当前sku商品关联的spu
    # sku就是当前sku商品对象
    # specs就是当前sku商品的规格和选项信息
    return goods, sku, specs