import random
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

options = Options()
options.add_argument("--start-maximized")
driver = WebDriver(options=options)
# time_to_wait = random.randint(15, 20)
# print('time_to_wait: ', time_to_wait)
# driver.implicitly_wait(time_to_wait)

driver.get("http://weibo.com")

# time.sleep(time_to_wait)

wait = WebDriverWait(driver, 30)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.wbpro-side-main')))
wait.until(EC.visibility_of(element))

for elem in driver.find_elements(by=By.CSS_SELECTOR, value='div.wbpro-side-panel'):
    print('_'.join(elem.text.split('\n')))
print('-----------------------完整热搜榜单-------------------------')
more = driver.find_element(by=By.CSS_SELECTOR, value='button.wbpro-side-btn')
# for m in more:
#     print(m.text)
more.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.HotTopic_tit_eS4fv')))
wait.until(EC.visibility_of(element))

for elem in driver.find_elements(by=By.CSS_SELECTOR, value='div.HotTopic_tit_eS4fv'):
    print('_'.join(elem.text.split('\n')))

driver.quit()
