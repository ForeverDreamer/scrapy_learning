# 每个spider应该可以对应多个产品，每个产品对应一个Item，每个Item对应各自的django model
import time

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from alicrawler.items import ProductItem
from scrapy_selenium import SeleniumRequest


class ProductSpider(scrapy.Spider):
    name = 'product_spider'

    # start_urls = ['http://127.0.0.1:8000/ct/ri']
    # start_urls = ['http://www.okbuy.com/p-nike/detail-shoe-17844839.html']
    def start_requests(self):

        # We scrape the first 5 pages of books to scrape
        urls = [
            'https://www.jd.com/',
            # 'https://list.jd.com/list.html?cat=670,671,672',
            # 'https://list.jd.com/list.html?cat=670,671,1105',
            # 'https://list.jd.com/list.html?cat=670,671,2694',
        ]

        # We generate a Request for each URL
        # We also specify the use of the parse function to parse the responses
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.navigate)
            # yield SeleniumRequest(url=url, callback=self.parse, cookies=[{'name': 'currency',
            #                                                               'value': 'USD',
            #                                                               'domain': 'example.com',
            #                                                               'path': '/currency'}])

    def navigate(self, response):
        # time.sleep(10)
        driver = response.request.meta['driver']
        # cookies = driver.get_cookies()
        # print(cookies)
        driver.implicitly_wait(10)
        action_chains = ActionChains(driver)
        computer_work = driver.find_element_by_xpath("//li[@data-index='3']")
        action_chains.move_to_element(computer_work).perform()
        note_book = driver.find_element_by_xpath('//*[@id="cate_item3"]/div[1]/div[2]/dl[1]/dd/a[1]')
        # action_chains = ActionChains(driver)
        # action_chains.move_to_element(note_book).click(note_book).perform()
        yield SeleniumRequest(url='https://list.jd.com/list.html?cat=670,671,672', callback=self.parse)

    def veri_code_show(self, driver):
        # 检测当前页面的验证元素，判断是否出现验证码
        return "验证码字符" in driver.page_source

    def parse(self, response):
        driver = response.request.meta['driver']
        # cookies = driver.get_cookies()
        # print(cookies)
        driver.implicitly_wait(10)
        # 如果网站弹出程序无法自动解决的验证码，可以通过人工辅助的方式输入验证码，然后重新获取当前网页数据
        if self.veri_code_show(driver):
            # 等待人工输入验证码后，重新请求当前页面
            while self.veri_code_show(driver):
                time.sleep(10)
            yield SeleniumRequest(url='https://list.jd.com/list.html?cat=670,671,672', callback=self.parse)
            return
        # time.sleep(5)
        product_list = response.css('li.gl-item')

        for product in product_list:
            product_loader = ItemLoader(item=ProductItem(), selector=product)

            product_loader.default_output_processor = TakeFirst()

            # product_loader.add_css('title', '#prodTitleName::text')
            # product_loader.add_css('desc', '#prodTitleName::text')
            # product_loader.add_css('price', '#prodPriceAj::text')
            product_loader.add_css('title', 'div.p-name i::text')
            product_loader.add_css('desc', 'div.p-name i::text')
            product_loader.add_css('price', 'div.p-price>strong>i::text')

            yield product_loader.load_item()

    def login(self, response):
        # 如果登录需要手机验证码
        veri_code = input('请输入验证码: ')
        # 填充验证码到输入框
        pass
