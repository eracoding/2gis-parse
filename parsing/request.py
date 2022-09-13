import csv
import time
import random
import os
import pandas as pd

from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

DRIVER_PATH = f'{os.getcwd()}\\chromedriver.exe'


def driver_initialize():
    options = webdriver.ChromeOptions()
    # options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--start-maximized")
    # options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20090101 FIrefox/83.0")
    # disable webdriver mode
    options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(executable_path=DRIVER_PATH)


def req_to2gis(driver, url, actions):
    driver.get(url=url)
    time.sleep(15)
    all_data = {}

    # close cookies
    driver.find_element(By.XPATH, "//footer/div/*[name()='svg']").click()
    time.sleep(random.randint(2, 7))

    # All rubrics main page to disclose
    driver.find_element(By.XPATH, "//a[@title='Рубрики']").click()
    time.sleep(random.randint(2, 7))

    # All rubrics TODO: MAKE IN A LOOP
    all_rubrics = driver.find_elements(By.XPATH, "//div[@style='width: 100%; height: 100%; border-radius: 0px;']")
    # for i in range(len(all_rubrics) - 1):
    #     print(all_rubrics[i].find_element(By.XPATH, ".//ancestor::a[@data-h='true']").get_attribute('title'))

    # rubrics url link
    rubrics_url = driver.current_url

    all_rubrics[0].click()

    time.sleep(random.randint(2, 4))
    name = all_rubrics[0].find_element(By.XPATH, ".//ancestor::a[@data-h='true']").get_attribute('title')
    all_data[name] = {}

    # click More
    driver.find_element(By.XPATH, "//div/a[@title='Ещё' and @data-h='true']").click()
    time.sleep(random.randint(2, 7))

    # Subcategory list
    subcat = driver.find_elements(By.XPATH,
                                  "//div[@tabindex='-1' and @data-scroll='true']/div[@class='_15gu4wr' and @style='width: 352px;']/div/div[@class='_13w22bi']")

    # subrubrics url link
    subrubrics_url = driver.current_url

    subrub = subcat[0].text.split('\n')[0]
    all_data[name][subrub] = {}

    subcat[0].click()
    # driver.get(subrubrics_url)
    # time.sleep(random.randint(2, 7))
    #
    # driver.get(rubrics_url)
    # time.sleep(15)
    for i in range(2):
        time.sleep(random.randint(2, 4))
        all_data = scrab_data(driver, actions, all_data, name, subrub)
        ogrn_data(driver, actions, all_data, name, subrub)
        print(all_data)
        csv_write(all_data)
        try:
            checkNextPage = driver.find_element(By.XPATH,
                                                "//div[@class='_7q94tr']/*[name()='svg' and @style='transform: rotate(-90deg);']")
            break
        except Exception as ex:
            pass

        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        time.sleep(random.randint(2, 4))
        nextPage = driver.find_element(By.XPATH, "//*[name()='svg' and @style='transform: rotate(-90deg);']")
        driver.implicitly_wait(random.randint(2, 7))
        nextPage.click()
        time.sleep(random.randint(2, 4))


def ogrn_data(driver, actions, all_data, rub, sub_rub):
    adverts = driver.find_elements(By.XPATH, "//div[@class='_awwm2v']/div[@class='_106bqvr']")
    for advert in adverts:
        ogrn, name = '-', '-'
        try:
            name = advert.find_element(By.XPATH, ".//div[@class='_1ltdkuc']/span").text
            ogrn = advert.find_element(By.XPATH, ".//div[@class='_1sih4tys']").get_attribute('title')
        except Exception as ex:
            pass
        finally:
            if 'ОГРН' in ogrn:
                ogrn = ogrn[ogrn.find('ОГРН'):]
            if name in all_data:
                all_data[rub][sub_rub][name]['ОГРН'] = ogrn


def scrab_data(driver, actions, all_data, rub, sub_rub):
    # time.sleep(random.randint(2, 7))
    companies = driver.find_elements(By.XPATH, "//div[@class='_uf1t8l' and @style='width: 56px;']")
    for company in companies:
        company.click()
        time.sleep(random.randint(2, 4))
        name, description, address, branches, address2, phonenumbers, webpages, emails = '-', '-', '-', '-', '', '-', '-', '-'
        tag_name, sprav = '-', ''
        tw, tg, vk, ok, yt, wa, pint, counter = '-', '-', '-', '-', '-', '-', '-', 0

        try:
            name = driver.find_element(By.XPATH,
                                       "//div[@class='_19sjw5q']/div/div/div[@class='_1dcp9fc']")
            name, tag_name = name.text.split('\n')
        except Exception as ex:
            pass
        finally:
            if name in all_data[rub][sub_rub]:
                actions.send_keys(Keys.PAGE_DOWN)
                actions.perform()
                time.sleep(2)
                try:
                    el = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='_49kxlr']/div[@class='_b0ke8']"))
                    )
                    el.click()
                    phonenumbers = driver.find_elements(By.XPATH, "//div[@class='_49kxlr']/div[@class='_b0ke8']")
                    phonenumbers = ', '.join(p.text for p in phonenumbers)
                except Exception as ex:
                    pass
                finally:
                    if phonenumbers != all_data[rub][sub_rub][name]['phone']:
                        all_data[rub][sub_rub][name]['phone'] += phonenumbers
                    driver.back()
                    continue
            all_data[rub][sub_rub][name] = {}
            all_data[rub][sub_rub][name]['tag_name'] = tag_name

        try:
            el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='_1s7yvxc']"))
            )
            el.click()
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            description = el.text
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['description'] = description

        driver.implicitly_wait(random.randint(2, 7))

        try:
            address = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='_13eh3hvq']/div/div/span[@class='_14quei']"))
            ).text

            if 'этаж' in address:
                pivot = address.find('этаж')
                address = address[:pivot - 2] + ', ' + address[pivot - 2:]

            branches = driver.find_element(By.XPATH, "//div[@class='_13eh3hvq']/div/div/span[@class='_14quei']/span/a[@class='_1rehek']").text
            address2 = driver.find_element(By.XPATH, "//div[@class='_13eh3hvq']/div/div/div[@class='_1p8iqzw']").text
        except Exception as ex:
            pass
        finally:
            if branches in address:
                address = address[:len(address) - len(branches)]
            all_data[rub][sub_rub][name]['address'] = address + ', ' + address2
            all_data[rub][sub_rub][name]['branches'] = branches

        time.sleep(2)
        try:
            el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='_49kxlr']/div[@class='_b0ke8']"))
            )
            el.click()
            phonenumbers = driver.find_elements(By.XPATH, "//div[@class='_49kxlr']/div[@class='_b0ke8']")
            phonenumbers = ', '.join(p.text for p in phonenumbers)

            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['phone'] = phonenumbers

        try:
            webpages = driver.find_elements(By.XPATH, "//div[@class='_49kxlr']/span/div/a[@target='_blank']")
            webpages = ', '.join(w.text for w in webpages)
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['website'] = webpages
        try:
            emails = driver.find_elements(By.XPATH, "//div[@class='_49kxlr']/div/a[contains(@href, 'mailto')]")
            emails = ', '.join((e.text for e in emails))
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['email'] = emails

        try:
            vk = driver.find_element(By.XPATH, "//a[@aria-label='ВКонтакте']")
            vk = vk.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['vk'] = vk

        try:
            tg = driver.find_element(By.XPATH, "//a[@aria-label='Telegram']")
            tg = tg.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['tg'] = tg

        try:
            tw = driver.find_element(By.XPATH, "//a[@aria-label='Twitter']")
            tw = tw.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['tw'] = tw

        try:
            ok = driver.find_element(By.XPATH, "//a[@aria-label='Одноклассники']")
            ok = ok.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['ok'] = ok

        try:
            yt = driver.find_element(By.XPATH, "//a[@aria-label='YouTube']")
            yt = yt.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['yt'] = yt

        try:
            wa = driver.find_element(By.XPATH, "//a[@aria-label='WhatsApp']")
            wa = wa.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['wa'] = wa

        try:
            pint = driver.find_element(By.XPATH, "//a[@aria-label='pinterest']")
            pint = pint.get_attribute('href')
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['pint'] = pint
        all_data[rub][sub_rub][name]['cur_url'] = driver.current_url

        try:
            # infobar
            infobar = driver.find_element(By.XPATH, "//div[@class='_jro6t0']/div/div/a[@class='_2lcm958']")
            infobar.click()

            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()

            time.sleep(2)
            sprav = driver.find_element(By.XPATH,
                                        "//div[@class='_172gbf8' and @data-divider='true']/div/div/span[@class='_14quei']/span/a[@class='_1rehek']")
            sprav = sprav.find_element(By.XPATH, ".//ancestor::span[@class='_14quei']")
            sprav = sprav.find_elements(By.XPATH, ".//span[@class='_er2xx9']")
            sprav = ', '.join(s.text for s in sprav)
        except Exception as ex:
            pass
        finally:
            all_data[rub][sub_rub][name]['sprav'] = sprav
            print(sprav)

        driver.back()
        driver.back()
        time.sleep(1)

        company.click()
        driver.back()
        time.sleep(1)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()

        time.sleep(random.randint(2, 4))

    return all_data


def csv_write(data):
    header = ["Рубрика", "Наименование организации", "Город", "Подрубрика 1", "Подрубрика 2", "Описание", "Кол-во филиалов",
              "Адрес", "Телефон",
              "Сайт", "Email", "Instagram", "Facebook", "Youtube", "Whatsapp", "Вконтакте", "Telegram", "Twitter", "Одноклассники", "Pinterest",
              "Справочник", "Ссылка 2GIS на организацию", "ОГРН"]

    with open('test2.csv', 'a', encoding='utf16', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter='|')

        print('csv_write')
        for k, v in data.items():
            for k1, v1 in v.items():
                for k2, v2 in v1.items():
                    writer.writerow({"Рубрика": k.replace('\n', ' '),
                                     "Наименование организации": k2.replace('\n', ' '),
                                     "Город": "Москва",
                                     "Подрубрика 1": k1.replace('\n', ' '),
                                     "Подрубрика 2": v2['tag_name'].replace('\n', ' '),
                                     "Описание": v2['description'].replace('\n', ' '),
                                     "Кол-во филиалов": v2['branches'].replace('\n', ' '),
                                     "Адрес": v2['address'].replace('\n', ' '),
                                     "Телефон": v2['phone'].replace('\n', ' '),
                                     "Сайт": v2['website'].replace('\n', ' '),
                                     "Email": v2['email'].replace('\n', ' '),
                                     "Instagram": '-', "Facebook": '-',
                                     "Youtube": v2['yt'],
                                     "Whatsapp": v2['wa'],
                                     "Вконтакте": v2['vk'],
                                     "Telegram": v2['tg'],
                                     "Twitter": v2['tw'],
                                     "Одноклассники": v2['ok'],
                                     "Pinterest": v2['pint'],
                                     "Справочник": v2['sprav'],
                                     "Ссылка 2GIS на организацию": v2['cur_url'],
                                     "ОГРН": '-'})


def create_csv():
    header = ["Рубрика", "Наименование организации", "Город", "Подрубрика 1", "Подрубрика 2", "Описание",
              "Кол-во филиалов",
              "Адрес", "Телефон",
              "Сайт", "Email", "Instagram", "Facebook", "Youtube", "Whatsapp", "Вконтакте", "Telegram", "Twitter",
              "Одноклассники", "Pinterest",
              "Справочник", "Ссылка 2GIS на организацию", "ОГРН"]

    with open('test2.csv', 'w', encoding='utf16', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter='|')

        writer.writeheader()


def make_hyper_urls(driver, df, string):
    for i in df[string].keys():
        if df[string][i] != '-':
            driver.get(url=df[string][i])
            newurl = driver.current_url
            if len(newurl) <= 255:
                df[string][i] = '=HYPERLINK("' + newurl + '")'
            else:
                df[string][i] = newurl


def hyper_csv(driver):
    df = pd.read_csv(".\\test2.csv", sep='|', encoding='utf-16')
    df['Ссылка 2GIS на организацию'] = '=HYPERLINK("' + df["Ссылка 2GIS на организацию"] + '")'

    for k in df['Сайт'].keys():
        if len(df['Сайт'][k].split(', ')) < 2 and df['Сайт'][k] != '-':
            df['Сайт'][k] = '=HYPERLINK("' + df['Сайт'][k] + '")'

    make_hyper_urls(driver, df, 'Instagram')
    make_hyper_urls(driver, df, 'Facebook')
    make_hyper_urls(driver, df, 'Youtube')
    make_hyper_urls(driver, df, 'Whatsapp')
    make_hyper_urls(driver, df, 'Вконтакте')
    make_hyper_urls(driver, df, 'Telegram')
    make_hyper_urls(driver, df, 'Twitter')
    make_hyper_urls(driver, df, 'Одноклассники')
    make_hyper_urls(driver, df, 'Pinterest')

    df.to_excel(".\\test2.xlsx", index=False)


def main():
    url = 'https://2gis.ru/moscow'
    driver = driver_initialize()
    actions = ActionChains(driver)
    create_csv()

    try:
        req_to2gis(driver, url, actions)
        hyper_csv(driver)
        pass
    except Exception as ex:
        pass
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()

# from selenium.webdriver.support.wait import WebDriverWait
#
# # DRIVER_PATH = f'D:\\Companies\\megafon\\projects\\2gis-parse\\parsing\\chromedriver.exe'
# # DRIVER_PATH = f'{os.getcwd()}\\chromedriver.exe'
# # # print(DRIVER_PATH)
# # useragent = UserAgent()
# #
# # options = webdriver.ChromeOptions()
# # # options.add_argument(f"user-agent={useragent.random}")
# # options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20090101 FIrefox/83.0")
# # # disable webdriver mode
# # options.add_argument("--disable-blink-features=AutomationControlled")
# # driver = webdriver.Chrome(executable_path=DRIVER_PATH)  # options=options
# #
# # url = 'https://2gis.ru/moscow'
# # url = 'https://news.mail.ru/society/52414532/?frommail=1&utm_partner_id=949'
# # url = 'https://2gis.ru/moscow/search/%D0%A1%D1%83%D1%88%D0%B8-%D0%B1%D0%B0%D1%80%D1%8B/rubricId/15791'
# # url = 'https://2gis.ru/moscow/search/%D0%A1%D1%83%D1%88%D0%B8-%D0%B1%D0%B0%D1%80%D1%8B/rubricId/15791/page/2'
# # url = 'https://2gis.ru/moscow/search/%D0%9F%D0%BE%D0%B5%D1%81%D1%82%D1%8C/firm/70000001033945822/37.586437%2C55.773902?m=37.630999%2C55.768664%2F10.35%2Fr%2F0.24'
# try:
#     driver.get(url=url)
#     time.sleep(150)
#
#     driver.find_element(By.XPATH, "//footer/div/*[name()='svg']").click()
#     driver.implicitly_wait(random.randint(2, 7))
#
#     # click More
#     imgMore = driver.find_element(By.XPATH, "//div/a[@title='Ещё' and @data-h='true']")
#     imgMore.click()
#     driver.implicitly_wait(random.randint(2, 7))
#
#     # Subcategory list
#     subcat = driver.find_elements(By.XPATH, "//div[@tabindex='-1' and @data-scroll='true']/div[@class='_15gu4wr' and @style='width: 352px;']/div/div[@class='_13w22bi']")
#     print(subcat[0].text)
#     subcat[0].click()
#     time.sleep(15)
#
#     # descr = driver.find_element(By.XPATH, '//span[contains(@class, "text")]')
#     # print(descr.text)
#
#     # if driver.find_element('id', 'acceptRiskButton'):
#     #     verify = driver.find_element('id', 'acceptRiskButton').click()
#     # time.sleep(5)
#     # WebDriverWait(driver, 20).until(
#     #     EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @style='transform: rotate(-90deg);']"))).click()
#     # descr = driver.find_element(By.XPATH, "//*[name()='svg' and @style='transform:rotate(-90deg)']")
#     # # driver.find_element(By.XPATH, "//svg[@style='transform: rotate(-90deg);']").click()
#     # driver.implicitly_wait(random.randint(2, 7))
#     # print(descr, descr.text)
#     # # print('descr = ', description)
#     # driver.implicitly_wait(random.randint(2, 7))
#     # descr.click()
#     # driver.implicitly_wait(random.randint(2, 7))
#     # print("AFTER CLICK")
#     # driver.implicitly_wait(random.randint(2, 7))
#
#     # items = driver.find_elements(By.XPATH, "//div[@style='width: 56px;']/div[@data-tips='true']")    # /div[@tabindex='-1']
#     # items[0].click()
#     # print(len(items))
#     # time.sleep(5)
#     #
#     # svgScroll = driver.find_elements(By.XPATH, "//div[@data-rack='true']/div[@data-divider='true']")
#     # print(len(svgScroll))
#     # svgScroll[0].click()
#     # print(svgScroll[3].text)
#     # svgScroll[3].click()
#     # print(svgScroll[3].text)
#
#     # for i in range(len(svgScroll)):
#     #     try:
#     #         svgScroll[i].click()
#     #     except WebDriverException:
#     #         pass
#     #     finally:
#     #         print(svgScroll[i].text)
#     # time.sleep(10)
#     #close
#     # driver.find_element(By.XPATH, "//div[@style='margin-bottom:8px;pointer-events:all']").click()
#     # driver.implicitly_wait(random.randint(2, 7))
#
#     #working
#     # driver.find_element(By.XPATH, "//footer/div/*[name()='svg']").click()
#     # driver.implicitly_wait(random.randint(2, 7))
#     # ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
#     # driver.implicitly_wait(random.randint(2, 7))
#     for i in range(100):
#     #     companies = driver.find_elements(By.XPATH, "//div[@style='width:56px']")
#     #     for index in range(len(companies)):
#     #         companies[index].click()
#     #
#     #
#         nextPage = driver.find_element(By.XPATH, "//*[name()='svg' and @style='transform: rotate(-90deg);']")
#         driver.implicitly_wait(random.randint(2, 7))
#     #     # descr.click()
#         ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
#         driver.implicitly_wait(random.randint(2, 7))
#         nextPage.click()
#         time.sleep(random.randint(5, 10))
#
#
#
#     # ActionChains(driver).move_to_element(descr).click(descr).perform()
#     # print('\n', descr.text)
#     # driver.implicitly_wait(random.randint(2, 7))
#     # print("AFTER CLICK")
#     # driver.implicitly_wait(random.randint(2, 7))
#
#     # for item in description:
#     #     print('item = ', item.text)
#     #     driver.implicitly_wait(random.randint(2, 7))
#
# except Exception as ex:
#     print(ex)
# finally:
#     driver.close()
#     driver.quit()
