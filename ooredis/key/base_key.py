# coding:utf-8

__all__ = ['BaseKey']

__metaclass__ = type

from ooredis.client import get_client
from ooredis.type_case import GenericTypeCase

class BaseKey:

    """ 
    所有其他 Key 对象的基类，保存了 key 名，客户端以及 TypeCase 。
    """

    ## add db
    def __init__(self, name, db_key, client=None, type_case=GenericTypeCase):
        """ 
        指定 key 名和客户端，以及 TypeCase 。

        Args:
            name: Redis key 的名字
            db: 数据库的名称
            client: 客户端，默认为全局客户端
            type_case: 类型转换类

        Time:
            O(1)

        Returns:
            None

        Raises:
            None
        """
        self.name = name
        self._client = client or get_client(db_key)
        self._encode = type_case.encode
        self._decode = type_case.decode


    def __eq__(self, other):
        """ 
        判断两个 Key 对象是否相等。

        Args:
            other: 另一个 Key 对象。

        Time:
            O(1)

        Returns:
            bool: 相等返回 True ，否则返回 False 。

        Raises:
            None
        """
        return self.name == other.name
