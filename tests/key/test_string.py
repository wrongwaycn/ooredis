#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

from ooredis import String
from ooredis.client import connect
from ooredis.key.helper import format_key

redis_dbs = {
    "test":{
        "host":'127.0.0.1',
        "db":0,
        }
    }

class TestString(unittest.TestCase):

    def setUp(self):
        connect("test",**redis_dbs["test"])

        self.redispy = redis.Redis()
        self.redispy.flushdb()
  
        self.name = 'pi'
        self.value = 3.14

        self.key = String(self.name,db_key="test")

    def tearDown(self):
        self.redispy.flushdb()


    # __repr__

    def test_repr(self):
        self.key.set(self.value)

        self.assertEqual(
            repr(self.key),
            format_key(self.key, self.name, self.value)
        )


if __name__ == "__main__":
    unittest.main()
