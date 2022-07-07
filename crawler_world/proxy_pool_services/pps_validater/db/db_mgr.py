from config.config_getter import config
from util.util_class import Singleton
from .redis_mgr import RedisClient
from .mongo_mgr import MongodbClient
from importlib import import_module
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DbClient:
    """
    DbClient DB工厂类 提供get/put/pop/delete/getAll/changeTable方法

    目前存放代理的table/collection/hash有两种：
        raw_proxy： 存放原始的代理；
        useful_proxy_queue： 存放检验后的代理；

    抽象方法定义：
        get(proxy): 返回proxy的信息；
        put(proxy): 存入一个代理；
        pop(): 弹出一个代理
        exists(proxy)： 判断代理是否存在
        getNumber(raw_proxy): 返回代理总数（一个计数器）；
        update(proxy, num): 修改代理属性计数器的值;
        delete(proxy): 删除指定代理；
        getAll(): 返回所有代理；
        changeTable(name): 切换 table or collection or hash;


        所有方法需要相应类去具体实现：
            SSDB：SsdbClient.py
            REDIS:redis_mgr.py  停用 统一使用SsdbClient.py

    """

    __metaclass__ = Singleton

    def __init__(self):
        self.client = None
        self._init_dbclient()

    def _init_dbclient(self):
        db_module = getattr(__import__('{}_mgr'.format(config.db_type)), '{}Client'.format(config.db_type.capitalize()))

        self.client = db_module(name=config.db_name,
                                host=config.db_host,
                                port=config.db_port,
                                password=config.db_password)

    def get(self, key, **kwargs):
        return self.client.get(key, **kwargs)

    def put(self, key, **kwargs):
        return self.client.put(key, **kwargs)

    def update(self, key, value, **kwargs):
        return self.client.update(key, value, **kwargs)

    def delete(self, key, **kwargs):
        return self.client.delete(key, **kwargs)

    def exists(self, key, **kwargs):
        return self.client.exists(key, **kwargs)

    def pop(self, **kwargs):
        return self.client.pop(**kwargs)

    def get_all(self):
        return self.client.get_all()

    def get_number(self):
        return self.client.get_number()

    def change_table(self, name):
        self.client.change_table(name)


if __name__ == "__main__":
    account = DbClient()
    account.changeTable('useful_proxy')
    print(account.pop())
