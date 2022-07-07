from os import getenv


class ConfigError(BaseException):
    pass


DB_TYPE = getenv('DB_TYPE', 'redis')

if DB_TYPE == 'redis':
    DB_HOST = getenv('REDIS_HOST', '192.168.49.135')
    DB_PORT = getenv('REDIS_PORT', '6379')
elif DB_TYPE == 'mongodb':
    DB_HOST = getenv('MONGODB_HOST', '127.0.0.1')
    DB_PORT = getenv('MONGODB_PORT', '27017')
else:
    raise ConfigError('Unknown database type, your environment variable `db_type` should be one of SSDB/MONGODB.')

DATABASES = {
    "TYPE": DB_TYPE,
    "HOST": DB_HOST,
    "PORT": DB_PORT,
    "NAME": "raw_proxy",
    "PASSWORD": ""
}

# register the proxy getter function

PROXY_GETTER = [
    "get_wuyou",
    # "get_66ip",
    "get_xici",
    # "freeProxySeventh",
    # "freeProxyTen",
    # "freeProxyEleven",
    # "freeProxyTwelve",
    # 以上待优化
    # "freeProxyFifth",
    # "freeProxyEight",
    # "freeProxyNinth",
    # "freeProxySixth"   # 不再提供免费代理
    # "freeProxyThird",  # 网站已不能访问
    # foreign website, outside the wall
    # "freeProxyWallFirst",
    # "freeProxyWallSecond",
    # "freeProxyWallThird"
]

SERVER_API = {
    "HOST": "0.0.0.0",  # The ip specified which starting the web API
    "PORT": 8000  # port number to which the server listens to
}

API_LIST = {
    'get': 'get an usable proxy',
    'get_all': 'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8000': 'delete an invalid proxy',
    'get_status': 'proxy statistics'
}
