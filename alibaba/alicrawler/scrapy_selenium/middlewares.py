"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""

import os
from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait

from .http import SeleniumRequest


class SeleniumMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, driver_name, driver_executable_path, driver_arguments, browser_executable_path, proxy_info):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        """

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_klass = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        if driver_arguments:
            for argument in driver_arguments:
                driver_options.add_argument(argument)

        if proxy_info.get('enable'):
            if proxy_info.get('password'):
                plugin_path = self.create_proxyauth_extension(
                    proxy_host="www.foo.com",
                    proxy_port=8010,
                    proxy_username="name",
                    proxy_password="password"
                )
                driver_options.add_extension(plugin_path)
            else:
                driver_options.add_argument(f'--proxy-server={self.get_proxy()}')

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        self.driver = driver_klass(**driver_kwargs)
        # cookies = self.driver.get_cookies()
        # print(cookies)
        self.driver.delete_all_cookies()

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')
        proxy_info = crawler.settings.get('SELENIUM_DRIVER_PROXY')

        if not driver_name or not driver_executable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path,
            proxy_info=proxy_info
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumRequest):
            return None

        # 自定义额外cookie，应该加在请求前(未测试，原来的代码为什么是在self.driver.get(request.url)之后，代码写错了？)
        for cookie in request.cookies:
            self.driver.add_cookie(cookie)

        self.driver.get(request.url)

        # for cookie_name, cookie_value in request.cookies.items():
        #     self.driver.add_cookie(
        #         {
        #             'name': cookie_name,
        #             'value': cookie_value
        #         }
        #     )

        # Saving current cookies and reformatting them
        # cookies = self.driver.get_cookies()
        # print(cookies)
        # cookies应该是driver自动管理的，一般不需要自己手动添加
        # for cookie in cookies:
        #     if 'expiry' in cookie:
        #         cookie['expiry'] = int(cookie['expiry'])

        # Adding cookies back into the driver
        # F12查看一下Chrome cookies，确认不要重复添加
        # for cookie in cookies:
        #     self.driver.add_cookie(cookie)

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(
                request.wait_until
            )

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()

    @staticmethod
    def get_proxy():
        # 从代理服务商获取可用ip
        proxy = 'http://localhost:8888'
        return proxy

    @staticmethod
    def create_proxyauth_extension(proxy_host, proxy_port,
                                   proxy_username, proxy_password,
                                   scheme='http', plugin_path=None):
        """Proxy Auth Extension

        args:
            proxy_host (str): domain or ip address, ie proxy.domain.com
            proxy_port (int): port
            proxy_username (str): auth username
            proxy_password (str): auth password
        kwargs:
            scheme (str): proxy scheme, default http
            plugin_path (str): absolute path of the extension

        return str -> plugin_path
        """
        import string
        import zipfile

        if plugin_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            plugin_path = os.path.join(base_dir, 'chrome_proxyauth_plugin.zip')

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        # background_js = """
        # var config = {
        #         mode: "fixed_servers",
        #         rules: {
        #         singleProxy: {
        #             scheme: "%s",
        #             host: "%s",
        #             port: parseInt(%s)
        #         },
        #         bypassList: ["localhost"]
        #         }
        #     };
        #
        # chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        #
        # function callbackFn(details) {
        #     return {
        #         authCredentials: {
        #             username: "%s",
        #             password: "%s"
        #         }
        #     };
        # }
        #
        # chrome.webRequest.onAuthRequired.addListener(
        #             callbackFn,
        #             {urls: ["<all_urls>"]},
        #             ['blocking']
        # );
        # """ % (scheme, proxy_host, proxy_port, proxy_username, proxy_password)

        background_js = string.Template(
            """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                      },
                      bypassList: ["foobar.com"]
                    }
                  };
    
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }
    
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """
        ).substitute(
            scheme=scheme,
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path
