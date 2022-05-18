import datetime
import random
import string

import requests
from appium.webdriver.common.touch_action import TouchAction
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import APP
from constants import USER_REFILL, USER_WITHDRAW
from wapi import get_user_wallets, refill, widget_withdraw, payment_api_deposit_request

TIME = 10


def fill_field(driver, element, text, clear=False):
    if not element_visible(driver, element):
        if APP == 'android':
            android_swipe_from_down_to_up(driver)
        if APP == 'ios':
            ios_swipe_from_down_to_up(driver)
    if clear:
        el = driver.find_element(*element).clear()
    el = wait_element(driver, element)
    el.send_keys(text)


def get_text(driver, element):
    return driver.find_element(*element).text


def get_attribute(driver, element, attribute):
    return driver.find_element(*element).get_attribute(attribute)


def wait_and_click(driver, element):
    el = WebDriverWait(driver, TIME).until(EC.element_to_be_clickable(element))
    el.click()


def click(driver, element):
    el = driver.find_element(*element)
    el.click()


def wait_element(driver, element):
    state = True
    count = 0
    while state and count < 3:
        try:
            el = WebDriverWait(driver, TIME).until(EC.visibility_of_element_located(element))
            state = False
            return el
        except TimeoutException:
            state = True
            count += 1


def click_keyboard_number(driver, element, numbers):
    for num in numbers:
        btn = wait_element(driver, (element[0], element[1] + num))
        btn.click()


def fill_phone_code(driver, element, numbers, count_retry_type=1):
    if numbers:
        for _ in range(0, count_retry_type):
            wait_element(driver, element)
            fill_field(driver, element, numbers)


def element_visible(driver, element):
    try:
        element = driver.find_element(*element)
        return element.is_displayed()
    except Exception:
        return False


def get_bool_platform():
    return True if APP == 'ios' else False


def element_presenter(driver, element):
    return False if len(driver.find_elements(*element)) == 0 else True


def ios_back_app(driver):
    TouchAction(driver).tap(x=59, y=39).perform()


def tap_to_screen(driver, x, y):
    TouchAction(driver).tap(x=x, y=y).perform()

def ios_swipe_from_down_to_up(driver):
    TouchAction(driver).press(x=380, y=744).wait(1000).move_to(x=386, y=91).release().perform()


def ios_swipe_middle_to_up(driver):
    TouchAction(driver).press(x=379, y=480).wait(1000).move_to(x=400, y=58).release().perform()


def wait_and_click_coordinate(driver, x, y):
    TouchAction(driver).tap(x=int(x), y=int(y)).perform()


def android_swipe_down_to_up(driver):
    TouchAction(driver).press(x=1023, y=1595).wait(1000).move_to(x=1007, y=357).release().perform()


def android_swipe_from_down_to_up(driver):
    TouchAction(driver).press(x=837, y=1923).wait(1000).move_to(x=887, y=259).release().perform()


def get_location(driver, element):
    return driver.find_element(*element).location


def get_email():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + '@test.ru'


def close_app(driver):
    driver.press_keycode(187)
    TouchAction(driver).press(x=519, y=1309).wait(1000).move_to(x=472, y=22).release().perform()
    TouchAction(driver).press(x=599, y=1437).wait(1000).move_to(x=650, y=194).release().perform()


def time_now():
    now = datetime.datetime.now()
    return now.strftime('%H:%M')

def restart_app(driver):
    driver.close_app()
    driver.launch_app()

def prepare_for_start(restart, driver):
    if restart:
        restart_app(driver)

def select_element(el1, el2):
    if APP == "android":
        return el2
    if APP == "ios":
        return el1

