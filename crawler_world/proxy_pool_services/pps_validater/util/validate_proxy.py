from threading import Thread
from util.util_function import valid_useful_proxy
from util.proxy_manager import ProxyManager
from util.log_handler import LogHandler

FAIL_COUNT = 3  # 校验失败次数， 超过次数删除代理


class ValidateProxy(Thread):
    """
    多线程验证useful_proxy
    """
    def __init__(self, queue, item_dict):
        self._pm = ProxyManager()
        super().__init__()
        self.log = LogHandler('validate_proxy', file=False)  # 多线程同时写一个日志文件会有问题
        self.queue = queue
        self.item_dict = item_dict

    def run(self):
        self._pm.db.change_table(self._pm.useful_proxy_queue)
        while self.queue.qsize():
            proxy = self.queue.get()
            if valid_useful_proxy(proxy):
                # 验证通过，从计数字典删除
                self.log.info('ProxyCheck: {} validation pass'.format(proxy))
                del self.item_dict[proxy]
            else:
                # 验证失败，计数加1
                self.item_dict[proxy] += 1
                self.log.info('ProxyCheck: {} validation fail'.format(proxy))
                if self.item_dict[proxy] >= FAIL_COUNT:
                    # 超过最大失败次数，从计数字典和数据库删除
                    self.log.info('ProxyCheck: {} fail too many, delete!'.format(proxy))
                    del self.item_dict[proxy]
                    self._pm.db.delete(proxy)
                else:
                    # 未超过最大失败次数，放回队列
                    self.queue.put(proxy)
            self.queue.task_done()


if __name__ == '__main__':
    # p = ProxyCheck()
    # p.run()
    pass
