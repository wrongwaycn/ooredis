# coding: utf-8

__all__ = ['connect', 'get_client']

import redis

client = {}

def connect(key,*args, **kwargs):
    """ 
    连接 Redis 数据库，参数和 redis-py 的 Redis 类一样。
    """
    global client
    if key not in client:
        client[key] = redis.Redis(*args, **kwargs)

def get_client(key):
    """ 
    返回 OORedis 客户端。
    """
    global client

    if key not in client:
        connect(key)
        
    if client[key] is None:
        connect(key)

    return client[key]
