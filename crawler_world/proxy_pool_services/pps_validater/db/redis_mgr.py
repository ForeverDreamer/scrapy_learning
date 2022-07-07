from redis import Redis
import json
import random
import sys


class RedisClient:
    # 为了保持DbClient的标准
    # 在RedisClient里面接受username参数, 但不进行使用.
    # 因为不能将username通过kwargs传进redis.Redis里面, 会报错:
    # TypeError: __init__() got an unexpected keyword argument 'username'
    def __init__(self, name, host, port, **kwargs):
        self.name = name
        self.__conn = Redis(host=host, port=port, **kwargs)

    def get(self):
        key = self.__conn.hgetall(name=self.name)
        # return random.choice(key.keys()) if key else None
        # key.keys()在python3中返回dict_keys，不支持index，不能直接使用random.choice
        # 另：python3中，redis返回为bytes,需要解码
        rkey = random.choice(list(key.keys())) if key else None
        if isinstance(rkey, bytes):
            return rkey.decode('utf-8')
        else:
            return rkey
            # return self.__conn.srandmember(name=self.name)

    def put(self, key):
        key = json.dumps(key) if isinstance(key, (dict, list)) else key
        return self.__conn.hincrby(self.name, key, 1)
        # return self.__conn.sadd(self.name, value)

    def getvalue(self, key):
        value = self.__conn.hget(self.name, key)
        return value if value else None

    def pop(self):
        key = self.get()
        if key:
            self.__conn.hdel(self.name, key)
        return key
        # return self.__conn.spop(self.name)

    def delete(self, key):
        self.__conn.hdel(self.name, key)
        # self.__conn.srem(self.name, value)

    def inckey(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def get_all(self):
        # return self.__conn.hgetall(self.name).keys()
        # python3 redis返回bytes类型,需要解码
        if sys.version_info.major == 3:
            return [key.decode('utf-8') for key in self.__conn.hgetall(self.name).keys()]
        else:
            return self.__conn.hgetall(self.name).keys()
            # return self.__conn.smembers(self.name)

    def get_status(self):
        return self.__conn.hlen(self.name)
        # return self.__conn.scard(self.name)

    def get_number(self):
        return self.__conn.hlen(self.name)

    def change_table(self, name):
        self.name = name


if __name__ == '__main__':
    c = RedisClient(name='useful_proxy', host='127.0.0.1', port=6379, password=None)
    print(c.get_all())
