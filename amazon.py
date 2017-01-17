#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored
import json

with open("amazon.json") as json_file:
    credentials = json.load(json_file)

browser = webdriver.Chrome()
list_url = "https://www.amazon.com/gp/registry/wishlist/1SXW34VUHH6D9/"
browser.get(list_url)

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "nav-signin-tooltip"))
    )
finally:
    login_link = browser.find_element_by_id("nav-signin-tooltip").find_element_by_tag_name("a");
    login_link.click()

browser.find_element_by_id("ap_email").send_keys(credentials["email"])
browser.find_element_by_id("ap_password").send_keys(credentials["password"])
browser.find_element_by_id("signInSubmit").click()

def get_listed_prices():
    list_items = browser.find_elements_by_class_name("g-item-sortable")
    for item in list_items:
        name = item.find_element_by_class_name("g-itemImage").find_element_by_tag_name("a").get_attribute("title")
        price = item.find_element_by_class_name("a-color-price").text
        price = price.split()[0] if price else ''
        if len(price) > 1 and float(price[1:]) < 20:
            formatted_price = colored('{0:<8}'.format(price), 'green')
        else:
            formatted_price = '{0:<8}'.format(price)

        print(formatted_price, name)

get_listed_prices()
browser.get("https://www.amazon.com/gp/registry/wishlist/2HLZBE98I7FE6/")
get_listed_prices()

browser.close()

