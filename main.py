import csv
import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

START_URLS = ['https://www.kohls.com/',
              'https://www.barnesandnoble.com/',
              'https://www.beallsflorida.com/'
              ]
# TEMP_KEY = 'Lego 75316'
# TEMP_KEY2 = 'The Four Winds'
# TEMP_KEY3 = 'Womens Gel Venture 7'
KOHLS = 'https://www.kohls.com/search.jsp?submit-search=web-regular&search='
BEAllS = 'https://www.beallsflorida.com/SearchDisplay?categoryId=&storeId=10151&catalogId=12003&langId=-1&sType' \
         '=SimpleSearch&searchTerm= '
BARNES = 'https://www.barnesandnoble.com/s/'


def get_html(url):
    try:
        r = requests.get(url).text
        return r
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def sort_prices(l):
    l.sort(key=lambda x: x[1])
    return l


def write_to_csv(result_list):
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for l in result_list:
            writer.writerow(l)
    f.close()


def define_proxy():
    req_proxy = RequestProxy()
    proxies = req_proxy.get_proxy_list()
    us_proxies = []
    for p in proxies:
        if p.country == 'United States':
            us_proxies.append(p)
    proxy = random.choice(us_proxies).get_address()
    return proxy

def kohls_search_link(key):
    return KOHLS + key.strip().replace(' ', '+')


def bealls_search_link(key):
    return BEAllS + key.strip().replace(' ', '%20')


def barnesnoble_search_link(key):
    return BARNES + key.strip().replace(' ', '%20')


def search_3(keyword):
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = 'none'
    chrome_options.add_argument('user-agent=Chrome/80.0.3987.149')
    # proxy = define_proxy()
    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #     "httpProxy": proxy,
    #     "ftpProxy": proxy,
    #     "sslProxy": proxy,
    #     "proxyType": "MANUAL",
    # }
    # chrome_options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    results = []
    numbers = re.compile(r'\d+(?:\.\d+)?')
    try:
        website = 'Kohl\'s'
        # driver.get(START_URLS[0])
        # element = driver.find_element_by_xpath('//*[@id="search"]')
        # element.send_keys(keyword, Keys.ENTER)
        # driver.implicitly_wait(2)
        # title = driver.find_element(By.XPATH,
        #                             '/html/body/div[2]/div[2]/div/div[2]/div/div/div[3]/div[1]/div[1]/h1').text
        # price = numbers.findall(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/div['
        #                                                       '3]/div[2]/div/div/div/div/div[2]/ul/li['
        #                                                       '1]/div/p/span').text)[0]
        # link = driver.current_url
        soup = BeautifulSoup(get_html(kohls_search_link(keyword)), 'html5lib')
        title = soup.find('h1', class_='product-title').text.strip()
        price = soup.find('span', class_='pdpprice-row2-main-text').text.strip()
        link = soup.find('link', rel='canonical')['href']
        results.append([title, price, website, link])
        driver.quit()
        return results
    except:
        results.append([f'Your search for {keyword} did not match any products on {website}.', '', '', ''])
    try:
        website = 'Bealls'
        # driver.get(START_URLS[2])
        # driver.maximize_window()
        # element = driver.find_element_by_xpath(
        #     '/html/body/div[6]/div[2]/header/div[3]/div/div[2]/div/form/div[1]/input')
        # element.send_keys(keyword, Keys.ENTER)
        # driver.implicitly_wait(2)
        # # title = driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/div/div[1]/div[4]/div[2]/div/div[1]/div['
        # #                                      '2]/ul/li[1]/div/div[4]/a').text
        # title = driver.find_element_by_class_name('pr-prod-text').get_attribute('a').text
        # # price = numbers.findall(driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/div/div[1]/div[4]/div['
        # #                                                       '2]/div/div[1]/div[2]/ul/li[1]/div/div[5]/span['
        # #                                                       '3]').text)[0]
        # price = numbers.findall(driver.find_element_by_class_name('price').get_attribute('span').text)[0]
        # link = driver.find_element_by_class_name('pr-prod-text').get_attribute('href')
        soup = BeautifulSoup(get_html(bealls_search_link(keyword)), 'html5lib')
        title = soup.find('div', class_='dataLayer-productClick product-block1').find('div', class_='product-name '
                                                                                                    'match-height'
                                                                                                    '-element').find(
            'a').text.strip()
        link = soup.find('div', class_='dataLayer-productClick product-block1').find('div', class_='product-name '
                                                                                                   'match-height'
                                                                                                   '-element').find(
            'a')['href']
        price = soup.find('div', class_='dataLayer-productClick product-block1').find('div',
                                                                                      class_='product-price '
                                                                                             'match-height-element').find(
            'span', class_='price').text.strip()
        numbers = re.compile(r'\d+(?:\.\d+)?')
        results.append([title, numbers.findall(price)[0], website, link])
        driver.quit()
        return results
    except:
        results.append([f'Your search for {keyword} did not match any products on {website}.', '', '', ''])
    try:
        website = 'Barnes & Noble'
        driver.get(START_URLS[1])
        driver.maximize_window()
        element = driver.find_element_by_xpath('//*[@id="rhf_header_element"]/nav/div/div[3]/form/div/div['
                                               '2]/div/input[1]')
        element.send_keys(keyword, Keys.ENTER)
        driver.implicitly_wait(1)
        title = driver.find_element(By.CLASS_NAME, 'product-shelf-title').text
        price = numbers.findall(driver.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div['
                                                              '2]/div/div/section[2]/div/div[1]/div[2]/div['
                                                              '4]/div/a/span[2]').text)[0]
        link = driver.find_element_by_xpath('/html/body/main/div[3]/div[1]/div[2]/div[2]/div/div/section[2]/div/div['
                                            '1]/div[2]/div[1]/a').get_attribute('href')
        results.append([title, price, website, link])
        driver.quit()
        return results
    except:
        results.append([f'Your search for {keyword} did not match any products on {website}.', '', '', ''])
    driver.quit()
    return results
