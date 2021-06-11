from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as A
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

sleep(1)


def set_wishlist():

    amount = input("How many items are you buying today? \n")
    WishList = []

    while len(WishList) < int(amount):
        item = input("Input your wishlist items: \n")
        WishList.append(item)

    print(WishList)
    return WishList


class login_credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def sign_in(self):

        driver.get("https://www.amazon.com")
        driver.maximize_window()
        driver.implicitly_wait(3)

        amz_sign_in = driver.find_element_by_xpath("//*[@id='nav-link-accountList']")

        A(driver).move_to_element(amz_sign_in).click().perform()

        login = driver.find_element_by_name("email")
        login.send_keys(self.username)
        driver.implicitly_wait(3)
        login.send_keys(Keys.RETURN)
        driver.implicitly_wait(3)
        code = driver.find_element_by_name("password")
        driver.implicitly_wait(3)
        code.send_keys(self.password)
        driver.implicitly_wait(3)
        code.send_keys(Keys.RETURN)
        sleep(2)


def shopping_spree():
    wList = set_wishlist()

    for x in wList:
        search = driver.find_element_by_id("twotabsearchtextbox").send_keys(x)
        driver.implicitly_wait(3)
        button_search = driver.find_element_by_id("nav-search-submit-button")
        driver.implicitly_wait(3)
        A(driver).move_to_element(button_search).click().perform()
        driver.implicitly_wait(3)
        driver.execute_script("window.scrollTo(0, 500)")

        select = driver.find_element_by_class_name("s-image")
        driver.implicitly_wait(3)
        A(driver).move_to_element(select).click().perform()
        driver.implicitly_wait(3)

        add_to_cart = driver.find_element_by_id("add-to-cart-button")
        driver.implicitly_wait(3)
        A(driver).move_to_element(add_to_cart).click().perform()
        driver.implicitly_wait(3)
        erase = driver.find_element_by_id("twotabsearchtextbox")
        erase.send_keys(Keys.CONTROL, 'a')
        erase.send_keys(Keys.BACKSPACE)

    driver.implicitly_wait(10)


def check_out():
    budget2 = price_cap
    purchase = driver.find_element_by_id("nav-cart")
    A(driver).move_to_element(purchase).click().perform()
    driver.implicitly_wait(3)
    final_purchase = driver.find_element_by_xpath("//*[@id='sc-buy-box-ptc-button']/span/input")
    driver.implicitly_wait(3)
    A(driver).move_to_element(final_purchase).click().perform()
    driver.implicitly_wait(3)

    checkout_total = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/div/div/div/table/tbody/tr[7]/td[2]")

    print("Your total is: ", checkout_total.text)


shop = login_credentials("YOUR EMAIL HERE", "YOUR PASSWORD HERE")
shop.sign_in()
sleep(1)
shopping_spree()
sleep(1)
check_out()
