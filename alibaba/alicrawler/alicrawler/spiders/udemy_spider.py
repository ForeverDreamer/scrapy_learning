import time
import json
import os

import scrapy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# import pyautogui

from scrapy_selenium import SeleniumRequest

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UdemySpider(scrapy.Spider):
    name = 'udemy_spider'

    def start_requests(self):
        urls = [
            'https://www.udemy.com/',
        ]

        # We generate a Request for each URL
        # We also specify the use of the parse function to parse the responses
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.login)

    def parse(self, response):
        pass

    def login(self, response):
        driver = response.request.meta['driver']
        driver.implicitly_wait(10)

        try:
            login_btn = driver.find_element_by_xpath('//*[@id="udemy"]/div[1]/div[2]/div[1]/div[4]/div[4]/div/button')
        except NoSuchElementException:
            # login_btn = driver.find_element_by_css_selector('div.header--gap-xs--1q0SU')
            login_btn = driver.find_element_by_partial_link_text('login-popup')
        time.sleep(2)
        action_chains = ActionChains(driver)
        # action_chains.move_to_element(login_btn).click(login_btn).perform()
        action_chains.move_to_element(login_btn).perform()
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.click(login_btn).perform()
        time.sleep(5)

        with open(base_dir + '/utils/login_info.json') as f:
            login_info = json.load(f)
        email = login_info['email']
        passwd = login_info['passwd']

        email_input = driver.find_element_by_xpath('//*[@id="email--1"]')
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(email_input).perform()
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.click(email_input).perform()
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(1)

        passwd_input = driver.find_element_by_xpath('//*[@id="id_password"]')
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(passwd_input).perform()
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.click(passwd_input).perform()
        passwd_input.clear()
        time.sleep(2)
        passwd_input.send_keys(passwd)
        time.sleep(2)

        action_chains = ActionChains(driver)
        submit_btn = driver.find_element_by_xpath('//*[@id="submit-id-submit"]')
        action_chains.move_to_element(submit_btn).perform()
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.click(submit_btn).perform()
        # submit_btn.click()
        # action_chains = ActionChains(driver)
        # action_chains.move_to_element(note_book).click(note_book).perform()
        time.sleep(5)
