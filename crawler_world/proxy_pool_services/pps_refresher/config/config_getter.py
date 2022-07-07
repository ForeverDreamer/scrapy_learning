from util.util_class import LazyProperty
from config.setting import *


class ConfigGetter(object):
    """
    get config
    """

    def __init__(self):
        pass

    @LazyProperty
    def db_type(self):
        return DATABASES.get("TYPE")

    @LazyProperty
    def db_name(self):
        return DATABASES.get("NAME")

    @LazyProperty
    def db_host(self):
        return DATABASES.get("HOST")

    @LazyProperty
    def db_port(self):
        return DATABASES.get("PORT")

    @LazyProperty
    def db_password(self):
        return DATABASES.get("PASSWORD")

    @LazyProperty
    def proxy_getter_functions(self):
        return PROXY_GETTER

    @LazyProperty
    def web_ip(self):
        return SERVER_API.get("HOST", "127.0.0.1")

    @LazyProperty
    def web_port(self):
        return SERVER_API.get("PORT", 8000)

    @LazyProperty
    def get_api_list(self):
        return API_LIST


config = ConfigGetter()

if __name__ == '__main__':
    print(config.db_type)
    print(config.db_name)
    print(config.db_host)
    print(config.db_port)
    print(config.proxy_getter_functions)
    print(config.host_ip)
    print(config.host_port)
    print(config.db_password)
