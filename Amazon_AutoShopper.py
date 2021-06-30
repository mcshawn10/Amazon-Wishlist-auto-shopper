from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as A
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

sleep(1)


def web_scrape():
    price_combined = []
    item_titles = []
    combined_price = ""

    driver.implicitly_wait(2)
    all_product_info = driver.find_elements_by_css_selector(
        "div[class='a-section a-spacing-medium']")
    driver.implicitly_wait(2)
    print("Calculating cheapest item...")
    for product in all_product_info:

        try:
            product_name_display = product.find_element_by_css_selector(
                "span[class='a-size-base-plus a-color-base a-text-normal']").is_displayed()
            product_price_display = product.find_element_by_css_selector(
                "span[class='a-price']").is_displayed()

            if product_name_display == True and product_price_display == True:
                product_name_TEXT = product.find_element_by_css_selector(
                    "span[class='a-size-base-plus a-color-base a-text-normal']").text

                price_whole_TEXT = product.find_element_by_css_selector(
                    "span[class='a-price-whole']").text
                price_frac_TEXT = product.find_element_by_css_selector(
                    "span[class='a-price-fraction']").text

                combined_price = price_whole_TEXT + '.' + price_frac_TEXT
                combined_price = float(combined_price)

                item_titles.append(product_name_TEXT)
                price_combined.append(combined_price)

        except NoSuchElementException:
            continue

    print("$", min(price_combined))
    index_cheapest = price_combined.index(min(price_combined))
    cheapest_item_name = item_titles[index_cheapest]

    print(cheapest_item_name)

    return cheapest_item_name


def set_budget():
    price_cap = input("What is your budget today? \n $")
    price_cap = float(price_cap)
    return price_cap


def set_wishlist():
    WishList = []
    amount = input("Enter number amount of items: \n")

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

    budget = set_budget()
    wList = set_wishlist()
    chosen_item = ""

    for x in wList:
        search = driver.find_element_by_id("twotabsearchtextbox").send_keys(x)
        driver.implicitly_wait(3)
        button_search = driver.find_element_by_id("nav-search-submit-button")
        driver.implicitly_wait(3)
        A(driver).move_to_element(button_search).click().perform()
        driver.implicitly_wait(3)
        driver.execute_script("window.scrollTo(0, 700)")
        driver.implicitly_wait(3)

        chosen_item = web_scrape()
        driver.implicitly_wait(3)

        first_erase = driver.find_element_by_id("twotabsearchtextbox")
        first_erase.send_keys(Keys.CONTROL, 'a')
        first_erase.send_keys(Keys.BACKSPACE)

        driver.find_element_by_id("twotabsearchtextbox").send_keys(chosen_item)
        driver.implicitly_wait(3)
        second_search = driver.find_element_by_id("nav-search-submit-button")
        A(driver).move_to_element(second_search).click().perform()
        driver.implicitly_wait(3)


# CODE THAT ADDS ITEMS TO CART
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

    driver.implicitly_wait(3)
    check_out(budget)


def check_out(compare_price):

    purchase = driver.find_element_by_id("nav-cart")
    A(driver).move_to_element(purchase).click().perform()
    driver.implicitly_wait(3)
    final_purchase = driver.find_element_by_xpath("//*[@id='sc-buy-box-ptc-button']/span/input")
    driver.implicitly_wait(3)
    A(driver).move_to_element(final_purchase).click().perform()
    driver.implicitly_wait(3)

    checkout_total = driver.find_element_by_xpath(
        "//*[@id='subtotals-marketplace-table']/tbody/tr[7]/td[2]").text
    print("Your total is: ", checkout_total)
    checkout_total = list(checkout_total)
    checkout_total.remove('$')
    checkout_total_final = ''.join(checkout_total)
    checkout_total_final = float(checkout_total_final)

    if compare_price < checkout_total_final:
        print("Your total is over your budget, check your cart.")
    elif compare_price >= checkout_total_final:
        print("You are within your budget!")


shop = login_credentials("YOUR EMAIL HERE", "YOUR PASSWORD HERE")
shop.sign_in()
sleep(1)
shopping_spree()
sleep(1)
