# selenium 4
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import random
import logging
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.firefox.options import DesiredCapabilities
from http_request_randomizer.requests.proxy.ProxyObject import Protocol
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

import random
import logging
from time import sleep
from random import randint
from proxy_checking import ProxyChecker
from http_request_randomizer.requests.proxy.ProxyObject import Protocol
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


# def random_ssl_proxy_address():
#     # Obtain a list of HTTPS proxies
#     # Suppress the console debugging output by setting the log level
#     req_proxy = RequestProxy(log_level=logging.ERROR, protocol=Protocol.HTTPS)

#     # Obtain a random single proxy from the list of proxy addresses
#     random_proxy = random.sample(req_proxy.get_proxy_list(), 1)

#     return random_proxy[0].get_address()


# def get_proxy_address():
#     proxy_address = random_ssl_proxy_address()
#     checker = ProxyChecker()
#     proxy_judge = checker.check_proxy(proxy_address)
#     proxy_status = [value for key, value in proxy_judge.items() if key == 'status']

#     if proxy_status[0]:
#         return proxy_address
#     else:
#         print('Looking for a valid proxy address.')

#         # this sleep timer is helping with some timeout issues
#         # that were happening when querying
#         sleep(randint(5, 10))

#         get_proxy_address()


# random_ssl_proxy = get_proxy_address()
# print(f'Valid proxy address: {random_ssl_proxy}')


chrome_options = Options()
chrome_options.add_argument("log-level=3")
chrome_options.binary_location = 'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\Brave.exe'
ua = UserAgent()
a = ua.random
user_agent = ua.random
# print(user_agent)
chrome_options.add_argument(f'user-agent={user_agent}')
try:
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), keep_alive=True, options=chrome_options)
except:
    # chrome_options = Options()
    # chrome_options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(options=chrome_options, service=Service(
        ChromeDriverManager().install()), keep_alive=True)

# firefox_capabilities = DesiredCapabilities().CHROME
# # Suppress the console debugging output by setting the log level
# req_proxy = RequestProxy(log_level=logging.ERROR, protocol=Protocol.HTTPS)
# # Obtain a random single proxy from the list of proxy addresses
# random_proxy = random.sample(req_proxy.get_proxy_list(), 1)
# # add the random proxy to firefox_capabilities
# proxies = Proxy()
# proxies.ssl_proxy = random_proxy[0].get_address()
# proxies.add_to_capabilities(firefox_capabilities)

driver.get("https://balance.vanillagift.com/")
with open("cards.txt") as cards:
    for card in cards:
        try:
            card_number = driver.find_element(by=By.CSS_SELECTOR, value="#cardnumber")
            month_entry = driver.find_element(by=By.CSS_SELECTOR, value="#expMonth")
            year_entry = driver.find_element(by=By.CSS_SELECTOR, value="#expirationYear")
            cvv_entry = driver.find_element(by=By.CSS_SELECTOR, value="#cvv")
            button = driver.find_element(by=By.CSS_SELECTOR, value="#brandLoginForm_button")
        except:
            pass
        try:
            number = card[:str.find(card,":")]
            month = card[len(number)+1:len(number)+3]
            year = card[len(number)+len(month)+2:len(number)+len(month)+4]
            cvv = card[len(number)+len(month)+len(year)+3:]
            print("{0}:{1}:{2}:{3}".format(number,month,year,cvv))
            
            card_number.send_keys(number)
            month_entry.send_keys(month)
            year_entry.send_keys(year)
            cvv_entry.send_keys(cvv)
            
            sleep(2)
            
            button.click()
            sleep(3)
            balance = driver.find_element(by=By.CSS_SELECTOR, value="#balanceTrans > div > div > div.transactions")
            with open("balances.txt") as bal:
                bal.write("cvv={0},balance={1}".format(cvv, balance.text))
            try:
                captcha = driver.find_element(
                    by=By.CSS_SELECTOR, value="#rc-imageselect")
                print("captcha detected, please solve it to continue")
                done = input('input "d" when you are done: ')
            except:
                pass
            
            try:
                captcha = driver.find_element(
                    by=By.CSS_SELECTOR, value="#appBody > app-root > app-notification > div")
                print("card not accepted")
            except:
                pass
        except:
            print("card not accepted")
