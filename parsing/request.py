import time
import random

from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By  #find_element(By.XPATH, 'q')
from selenium.webdriver.common.action_chains import ActionChains
import os

from selenium.webdriver.support.wait import WebDriverWait

# DRIVER_PATH = f'D:\\Companies\\megafon\\projects\\2gis-parse\\parsing\\chromedriver.exe'
DRIVER_PATH = f'{os.getcwd()}\\chromedriver.exe'
# print(DRIVER_PATH)
useragent = UserAgent()

options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={useragent.random}")
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20090101 FIrefox/83.0")
# disable webdriver mode
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=DRIVER_PATH,
                          options=options)

# url = 'https://2gis.ru/moscow'
# url = 'https://news.mail.ru/society/52414532/?frommail=1&utm_partner_id=949'
url = 'https://2gis.ru/moscow/search/%D0%A1%D1%83%D1%88%D0%B8-%D0%B1%D0%B0%D1%80%D1%8B/rubricId/15791'
# url = 'https://2gis.ru/moscow/search/%D0%A1%D1%83%D1%88%D0%B8-%D0%B1%D0%B0%D1%80%D1%8B/rubricId/15791/page/2'
# url = 'https://2gis.ru/moscow/search/%D0%9F%D0%BE%D0%B5%D1%81%D1%82%D1%8C/firm/70000001033945822/37.586437%2C55.773902?m=37.630999%2C55.768664%2F10.35%2Fr%2F0.24'
try:
    driver.get(url=url)
    time.sleep(15)

    # descr = driver.find_element(By.XPATH, '//span[contains(@class, "text")]')
    # print(descr.text)

    # if driver.find_element('id', 'acceptRiskButton'):
    #     verify = driver.find_element('id', 'acceptRiskButton').click()
    # time.sleep(5)
    # WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @style='transform: rotate(-90deg);']"))).click()
    # descr = driver.find_element(By.XPATH, "//*[name()='svg' and @style='transform:rotate(-90deg)']")
    # # driver.find_element(By.XPATH, "//svg[@style='transform: rotate(-90deg);']").click()
    # time.sleep(random.randint(2, 7))
    # print(descr, descr.text)
    # # print('descr = ', description)
    # time.sleep(random.randint(2, 7))
    # descr.click()
    # time.sleep(random.randint(2, 7))
    # print("AFTER CLICK")
    # time.sleep(random.randint(2, 7))

    items = driver.find_elements(By.XPATH, "//div[@style='width:56px']")    # /div[@tabindex='-1']
    items[0].click()
    print(len(items))
    time.sleep(5)

    svgScroll = driver.find_elements(By.XPATH, "//div[@data-rack='true']/div[@data-divider='true']")
    print(len(svgScroll))
    # svgScroll[0].click()
    # print(svgScroll[3].text)
    # svgScroll[3].click()
    # print(svgScroll[3].text)

    for i in range(len(svgScroll)):
        try:
            svgScroll[i].click()
        except WebDriverException:
            pass
        finally:
            print(svgScroll[i].text)
    time.sleep(100)
    #close
    driver.find_element(By.XPATH, "//div[@style='margin-bottom:8px;pointer-events:all']").click()
    time.sleep(random.randint(2, 7))

    #working
    # driver.find_element(By.XPATH, "//footer/div/*[name()='svg']").click()
    # time.sleep(random.randint(2, 7))
    # ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    # time.sleep(random.randint(2, 7))
    # for i in range(100):
    #     companies = driver.find_elements(By.XPATH, "//div[@style='width:56px']")
    #     for index in range(len(companies)):
    #         companies[index].click()
    #
    #
    #     nextPage = driver.find_element(By.XPATH, "//*[name()='svg' and @style='transform:rotate(-90deg)']")
    #     time.sleep(random.randint(2, 7))
    #     # descr.click()
    #     # ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    #     time.sleep(random.randint(2, 7))
    #     nextPage.click()
    #     time.sleep(random.randint(5, 10))



    # ActionChains(driver).move_to_element(descr).click(descr).perform()
    # print('\n', descr.text)
    # time.sleep(random.randint(2, 7))
    # print("AFTER CLICK")
    # time.sleep(random.randint(2, 7))

    # for item in description:
    #     print('item = ', item.text)
    #     time.sleep(random.randint(2, 7))

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
