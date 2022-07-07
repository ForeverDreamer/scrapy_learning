import sys
import time
# import logging
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from util.util_function import valid_useful_proxy, verify_proxy_format
from util.proxy_manager import ProxyManager
from util.log_handler import LogHandler
from config.config_getter import config
from util.get_free_proxy import GetFreeProxy

# for docker env
sys.path.append('..')
# logging.basicConfig()


class ProxyRefresher:
    """
    代理定时刷新
    """
    def __init__(self):
        self._pm = ProxyManager()
        self.log = LogHandler('proxy_refresher')

    def fetch_all_proxy(self):
        """
        fetch proxy into Db by ProxyGetter/get_free_proxy.py
        :return:
        """
        for proxyGetter in config.proxy_getter_functions:
            # fetch
            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                # for proxy in getattr(GetFreeProxy, proxyGetter.strip())(self.get()):
                for proxy in getattr(GetFreeProxy, proxyGetter.strip())(None):
                    # 直接存储代理, 不用在代码中排重, hash 结构本身具有排重功能
                    proxy = proxy.strip()
                    if proxy and verify_proxy_format(proxy):
                        self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                        self._pm.db.change_table(self._pm.raw_proxy_queue)
                        self._pm.db.put(proxy)
                    else:
                        self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))
                        pass
            except Exception as e:
                self.log.error("{func}: fetch proxy fail, {e}".format(func=proxyGetter, e=e))
                continue

    def validate_raw_proxy(self):
        """
        验证raw_proxy_queue中的代理, 将可用的代理放入useful_proxy_queue
        :return:
        """
        self._pm.db.change_table(self._pm.raw_proxy_queue)
        raw_proxy = self._pm.db.pop()
        self.log.info('ProxyRefresher: %s start validProxy' % time.ctime())
        # 计算剩余代理，用来减少重复计算
        remaining_proxies = self._pm.get_all()
        while raw_proxy:
            if (raw_proxy not in remaining_proxies) and valid_useful_proxy(raw_proxy):
                self._pm.db.change_table(self._pm.useful_proxy_queue)
                self._pm.db.put(raw_proxy)
                self.log.info('ProxyRefresher: %s validation pass' % raw_proxy)
            else:
                self.log.info('ProxyRefresher: %s validation fail' % raw_proxy)
            self._pm.db.change_table(self._pm.raw_proxy_queue)
            raw_proxy = self._pm.db.pop()
            remaining_proxies = self._pm.get_all()
        self.log.info('ProxyRefresher: %s validProxy complete' % time.ctime())


def refresh_pool():
    pp = ProxyRefresher()
    pp.validate_raw_proxy()


def multi_thread_validate(process_num=50):
    # 检验新代理(python全局解释锁只能保证单核cpu不冲突，多线程同时对redis进行写操作需要自己加锁吗？或者redis本身就有加锁功能？)
    pl = []
    for num in range(process_num):
        proc = Thread(target=refresh_pool, args=())
        pl.append(proc)

    for num in range(process_num):
        pl[num].daemon = True
        pl[num].start()

    for num in range(process_num):
        pl[num].join()


def fetch_all_proxy():
    p = ProxyRefresher()
    p.fetch_all_proxy()


def run():
    scheduler = BackgroundScheduler()
    # 不用太快, 网站更新速度比较慢, 太快会加大验证压力, 导致raw_proxy积压
    scheduler.add_job(fetch_all_proxy,  'interval', minutes=30, id="fetch_all_proxy")
    scheduler.add_job(multi_thread_validate, "interval", minutes=1, id="multi_thread_validate")
    scheduler.start()

    fetch_all_proxy()
    multi_thread_validate()
    # refresh_pool()

    while True:
        time.sleep(3)


if __name__ == '__main__':
    run()
