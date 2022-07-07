import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

option = webdriver.ChromeOptions()
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)
driver.implicitly_wait(10)
driver.get("https://www.jd.com/")
action_chains = ActionChains(driver)
elem1 = driver.find_element_by_xpath("//li[@data-index='1']")
action_chains.move_to_element(elem1)
elem2 = driver.find_element_by_xpath("//li[@data-index='2']")
action_chains.move_to_element(elem2)
elem3 = driver.find_element_by_xpath("//li[@data-index='3']")
action_chains.move_to_element(elem3)
elem4 = driver.find_element_by_xpath("//li[@data-index='4']")
action_chains.move_to_element(elem4).perform()
# copy xpath
elem5 = driver.find_element_by_xpath('//*[@id="cate_item4"]/div[1]/div[2]/dl[2]/dd/a[2]')
action_chains = ActionChains(driver)
action_chains.move_to_element(elem5).click(elem5).perform()
driver.back()
# elem.click()
# alert = driver.switch_to.alert()
driver.close()
