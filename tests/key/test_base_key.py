#! /usr/bin/env python2.7
# coding:utf-8

import redis
import unittest

from ooredis.key.base_key import BaseKey
from ooredis.const import REDIS_TYPE
from ooredis.type_case import GenericTypeCase
from ooredis.client import connect, get_client

redis_dbs = {
    "test":{
        "host":'127.0.0.1',
        "db":0,
        }
    }

class TestBaseKey(unittest.TestCase):
    
    def setUp(self):
        connect("test",**redis_dbs["test"])
    
        self.name = "name"
        self.value = "value"

        self.key = BaseKey(self.name,db_key="test")

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()


    # __init__

    def test_init_key(self):
        self.assertTrue(
            isinstance(self.key._client, redis.Redis)
        )

        self.assertEqual(
            get_client("test"),
            self.key._client
        )

        self.assertEqual(
            self.key._encode,
            GenericTypeCase.encode
        )
        self.assertEqual(
            self.key._decode,
            GenericTypeCase.decode
        )


    # __eq__

    def test__eq__TRUE(self):
        self.assertEqual(
            self.key, 
            BaseKey(self.name,db_key="test")
        )

    def test__eq__FALSE(self):
        self.assertNotEqual(
            self.key,
            BaseKey('another-key',db_key="test")
        )

if __name__ == "__main__":
    unittest.main()
