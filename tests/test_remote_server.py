#! /usr/bin/env python2.7
# coding:utf-8

import unittest

from ooredis import connect,get_client,String
## connect = ooredis.connect
## get_client = ooredis.get_client
## String = ooredis.String
import redis

redis_dbs = {
    "test":{
        "host":'127.0.0.1',
        "db":0,
        }
    }

class TestRemoteServer(unittest.TestCase):
    
    def setUp(self):
        # ooredis
        connect("test",**redis_dbs["test"])
       
        # redis-py
        self.r = redis.Redis(**redis_dbs["test"])
        self.r.flushdb()

    def test_set_and_get(self):
        self.s = String('key',db_key="test")
        self.s.set('value')

        self.assertEqual(self.s.get(), 'value')

        self.assertTrue(self.r.exists('key'))
        self.assertEqual(self.r.get('key'), self.s.get())

if __name__ == "__main__":
    unittest.main()
