"""
封装cookie购物车加解密模块
"""

import pickle,base64

# 当前CookieSecret类无需实例化，仅仅用来封装加解密的2个函数/方法
class CookieSecret(object):

    @staticmethod
    def dumps(cart_dict):
        # 功能：加密
        # 参数：购物车字典cart_dict —— {1: {"count": 5, "selected": True}}
        # 返回值：购物车cookie字符串数据
        # (1)、购物车字典通过pickle编码
        data_bytes = pickle.dumps(cart_dict)
        # (2)、在经过base64编码
        base64_bytes = base64.b64encode(data_bytes) # b'EJNKHBfjnrebgfhjerbBHJB=='
        # (3)、返回cookie购物车字符串数据
        return base64_bytes.decode() # 'EJNKHBfjnrebgfhjerbBHJB=='

    @staticmethod
    def loads(cookie_str):
        # 功能：解密
        # 参数：购物车cookie字符串数据cookie_str —— 'EJNKHBfjnrebgfhjerbBHJB=='
        # 返回值：返回购物车字典数据
        # (1)、base64解码
        base64_bytes = base64.b64decode(cookie_str.encode())
        # (2)、pickle解码
        cart_dict = pickle.loads(base64_bytes)
        # (3)、返回购物车字典
        return cart_dict