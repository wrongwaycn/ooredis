#! /usr/bin/env python2.7
# coding:utf-8

import unittest

from ooredis.client import connect, get_client
import redis

redis_dbs = {
    "test":{
        "host":'127.0.0.1',
        "db":0,
        }
    }


class TestClient(unittest.TestCase):
    
    def setUp(self):
        self.client = connect("test",**redis_dbs["test"])

    def test_get(self):
        self.assertTrue(isinstance(get_client("test"), redis.Redis))

    def test_get_get(self):
        self.assertEqual(get_client("test"), get_client("test"))

if __name__ == "__main__":
    unittest.main()
