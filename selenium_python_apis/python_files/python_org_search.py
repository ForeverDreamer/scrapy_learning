# -*- coding: utf-8 -*-
# 2.1. Simple Usage

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import sys
# sys.path.append('C:/Users/doer/dev/tools')
# 把 chromedriver.exe 放到 C:\Users\doer\Anaconda3\envs\python_dev 或其它位于sys.path中的路径

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
