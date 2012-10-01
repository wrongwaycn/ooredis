# coding:utf-8

import redis
import unittest

from ooredis.key.base_key import BaseKey
from ooredis.key.common_key_property_mixin import CommonKeyPropertyMixin
from ooredis.const import REDIS_TYPE
from ooredis.type_case import GenericTypeCase
from ooredis.client import connect, get_client

redis_dbs = {
    "test":{
        "host":'127.0.0.1',
        "db":0,
        }
    }

class KeyWithProperty(BaseKey, CommonKeyPropertyMixin):
    pass

class TestCommonKeyPropertyMixin(unittest.TestCase):
    
    def setUp(self):
        connect("test",**redis_dbs["test"])
    
        self.name = "name"
        self.value = "value"

        self.key = KeyWithProperty(self.name,"test")

        self.redispy = redis.Redis(**redis_dbs["test"])
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()


    # _represent

    def test_represent(self):
        # string
        self.redispy.set('string', 'string')
        self.assertEqual(
            KeyWithProperty('string',"test")._represent,
            REDIS_TYPE['string']
        )

        # list
        self.redispy.lpush('list', 'itme')
        self.assertEqual(
            KeyWithProperty('list',"test")._represent,
            REDIS_TYPE['list']
        )

        # set
        self.redispy.sadd('set', 'element')
        self.assertEqual(
            KeyWithProperty('set',"test")._represent,
            REDIS_TYPE['set']
        )

        # sorted set
        self.redispy.zadd('sorted_set', 'value', 30)
        self.assertEqual(
            KeyWithProperty('sorted_set',"test")._represent,
            REDIS_TYPE['sorted_set']
        )

        # hash
        self.redispy.hset('hash', 'field', 'value')
        self.assertEqual(
            KeyWithProperty('hash',"test")._represent,
            REDIS_TYPE['hash']
        )

        # not exists key
        self.assertFalse(
            self.redispy.exists('not_exists_key')
        )
        self.assertEqual(
            KeyWithProperty('not_exists_key',"test")._represent,
            REDIS_TYPE['not_exists']
        )


    # ttl

    def test_ttl_with_PERSIST_KEY(self):
        self.redispy.set(self.key.name, self.value)

        self.assertIsNone(
            self.key.ttl
        )

    def test_ttl_with_VOLATILE_KEY(self):
        self.redispy.expire(self.key.name, 300)

        self.assertTrue(
            self.key.ttl <= 300
        )

    def test_ttl_with_NOT_EXISTS_KEY(self):
        self.redispy.delete(self.key.name)

        self.assertIsNone(
            self.key.ttl
        )


    # exists

    def test_exists_FALSE(self):
        self.assertFalse(
            self.key.exists
        )

    def test_exists_TRUE(self):
        self.redispy.set(self.key.name, self.value)

        self.assertTrue(
            self.key.exists
        )


    # delete

    def test_delete_EXISTS_KEY(self):
        self.redispy.set(self.key.name, self.value)

        self.key.delete()

        self.assertFalse(
            self.key.exists
        )

    def test_delete_NOT_EXISTS_KEY(self):
        self.key.delete()

        self.assertFalse(
            self.key.exists
        )


    # expire

    def test_expire_with_EXISTS_KEY(self):
        self.redispy.set(self.key.name, self.value)

        self.key.expire(30000)

        self.assertTrue(
            self.key.ttl <= 30000
        )

    def test_expire_RAISE_when_KEY_NOT_EXISTS(self):
        with self.assertRaises(TypeError):
            self.key.expire(30000)


    # expireat

    def test_expireat_with_EXISTS_KEY(self):
        self.redispy.set(self.key.name, self.value)

        self.key.expireat(1355292000)

        self.assertIsNotNone(
            self.key.ttl
        )

    def test_expireat_RAISE_when_KEY_NOT_EXISTS(self):
        with self.assertRaises(TypeError):
            self.key.expireat(1355292000)   # 2012.12.12


    # persist

    def test_persist_RAISE_when_KEY_NOT_EXISTS(self):
        with self.assertRaises(Exception):
            self.key.persist()

    def test_persist_with_PERSIST_KEY(self):
        self.redispy.set(self.key.name, self.value)

        self.assertIsNone(
            self.key.persist()
        )

    def test_persist_with_VOLATILE_KEY(self):
        self.redispy.setex(self.key.name, self.value, 3000)

        self.key.persist()

        self.assertIsNone(
            self.key.ttl
        )


if __name__ == "__main__":
    unittest.main()
