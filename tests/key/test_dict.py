#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

from ooredis.key.dict import Dict
from ooredis.client import connect
from ooredis.key.helper import format_key
from ooredis.type_case import JsonTypeCase

redis_dbs = {
    "test":{
        "host":'127.0.0.1',
        "db":0,
        }
    }



class TestDict(unittest.TestCase):
    
    def setUp(self):
        connect("test",**redis_dbs["test"])

        self.redispy = redis.Redis()
        self.redispy.flushdb()

        self.name = 'dict'
        self.key = 'key'
        self.value = [1, 2, 3]

        self.d = Dict(self.name,db_key="test", type_case=JsonTypeCase)

    def tearDown(self): 
        self.redispy.flushdb()

    def set_wrong_type(self, key):
        self.redispy.set(key.name, 'string')


    # __repr__

    def test__repr__(self):
        self.assertEqual(
            repr(self.d),
            format_key(self.d, self.name, dict(self.d))
        )

    
    # __contains__

    def test__contains__return_True(self):
        self.d[self.key] = self.value

        self.assertTrue(
            self.key in self.d
        )

    def test__contains__return_False(self):
        self.assertFalse(
            self.key in self.d
        )


    # __setitem__

    def test__setitem__when_KEY_NOT_TAKEN(self):
        self.d[self.key] = self.value
        
        self.assertEqual(
            self.d[self.key],
            self.value
        )

        self.assertEqual(
            dict(self.d),
            {self.key: self.value}
        )

    def test__setitem__OVERWRITE_EXISTS_KEY(self):
        self.old_value = 'foo'

        self.d[self.key] = self.value

        self.assertEqual(
            self.d[self.key],
            self.value
        )

        self.assertEqual(
            dict(self.d),
            {self.key : self.value}
        )

    def test__setitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d[self.key] = self.value


    # __getitem__

    def test__getitem__with_EXISTS_KEY(self):
        self.d[self.key]= self.value

        self.assertEqual(
            self.d[self.key],
            self.value
        )

    def test__getitem__RAISE_when_KEY_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            self.d[self.key]

    def test__getitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d[self.key]


    # __delitem__

    def test__delitem__when_KEY_EXISTS(self):
        self.d[self.key] = self.value
        
        del self.d[self.key]

        self.assertTrue(
            self.key not in self.d
        )

        self.assertEqual(
            dict(self.d),
            {}
        )

    def test__delitem__RAISE_when_KEY_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            del self.d['not_exists_key']

    def test__delitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            del self.d['wrong_type_cant_be_delete']


    # __iter__

    def test__ite__with_EMPTY_DICT(self):
        self.assertEqual(
            list(self.d),
            []
        )

    def test__ite__with_NOT_EMPTY_DICT(self):
        self.d[self.key] = self.value

        self.assertEqual(
            list(self.d),
            [self.key]
        )

    def test__iter__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            list(self.d)


    # __len__

    def test__len__with_EMPTY_DICT(self):
        self.assertEqual(
            len(self.d),
            0
        )

    def test__len__with_NOT_EMPTY_DICT(self):
        self.d[self.key] = self.value

        self.assertEqual(
            len(self.d),
            1
        )

    def test__len__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            len(self.d)


if __name__ == "__main__":
    unittest.main()
