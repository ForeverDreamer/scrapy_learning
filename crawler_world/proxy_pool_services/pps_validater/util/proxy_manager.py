import random
from db.db_mgr import DbClient
# from Util.LogHandler import LogHandler


class ProxyManager:
    """
    ProxyManager
    """

    def __init__(self):
        self.db = DbClient()
        self.raw_proxy_queue = 'raw_proxy'
        # self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def get(self):
        """
        return a useful proxy
        :return:
        """
        self.db.change_table(self.useful_proxy_queue)
        item_list = self.db.get_all()
        if item_list:
            return random.choice(item_list)
        return None

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.change_table(self.useful_proxy_queue)
        self.db.delete(proxy)

    def get_all(self):
        """
        get all proxy from pool as list
        :return:
        """
        self.db.change_table(self.useful_proxy_queue)
        item_list = self.db.get_all()

        return item_list if item_list else list()

    def get_number(self):
        self.db.change_table(self.raw_proxy_queue)
        total_raw_proxy = self.db.get_number()
        self.db.change_table(self.useful_proxy_queue)
        total_useful_queue = self.db.get_number()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}
