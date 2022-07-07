import time

from queue import Queue
from util.validate_proxy import ValidateProxy
from util.proxy_manager import ProxyManager
from util.log_handler import LogHandler


class ProxyValidater:
    """
     验证useful_proxy_queue中的代理,将不可用的移出
    """
    def __init__(self):
        self._pm = ProxyManager()
        self.queue = Queue()
        self.proxy_list = None
        self.proxy_dict = dict()
        self.log = LogHandler('proxy_validater')

    def _valid_proxy(self, threads=50):
        """
        验证useful_proxy代理
        :param threads: 线程数
        :return:
        """
        thread_list = list()
        for index in range(threads):
            thread_list.append(ValidateProxy(self.queue, self.proxy_dict))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def put_queue(self):
        self._pm.db.change_table(self._pm.useful_proxy_queue)
        self.proxy_list = self._pm.db.get_all()
        for proxy in self.proxy_list:
            self.queue.put(proxy)
            self.proxy_dict[proxy] = 0

    def main(self):
        self.put_queue()
        while True:
            if not self.queue.empty():
                self.log.info("Start valid useful proxy")
                self._valid_proxy()
            else:
                self.log.info('Valid Complete! sleep 600 sec.')
                time.sleep(600)
                self.put_queue()


if __name__ == '__main__':
    p = ProxyValidater()
    p.main()
