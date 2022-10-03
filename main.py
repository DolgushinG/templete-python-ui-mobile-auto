import random
import string
import time

import allure
from bs4 import BeautifulSoup
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import httpx
import re
import logging
import tools
from conftest import PLATFORM_NAME, ENV

TIME = 30


@allure.step('Параметры заполнения')
def fill_field(driver, element, text, clear=False):
    swipe_up(driver, element)
    if clear:
        driver.find_element(*element).clear()
    el = wait_element(driver, element)
    try:
        el.send_keys(text)
    except AttributeError:
        driver.find_element(*element).send_keys(text)


def get_text(driver, element):
    el = wait_element(driver, element)
    return tools.remove_space_and_new_line(el.text)


def get_attribute(driver, element, attribute):
    return driver.find_element(*element).get_attribute(attribute)


@allure.step('Ждем и кликаем')
def wait_and_click(driver, element):
    WebDriverWait(driver, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException), timeout=TIME) \
        .until(EC.element_to_be_clickable(element)) \
        .click()


@allure.step('Кликаем')
def click(driver, element):
    el = driver.find_element(*element)
    el.click()


def wait_element(driver, element):
    try:
        return WebDriverWait(driver, TIME).until(EC.presence_of_element_located(element))
    except TimeoutException and NoSuchElementException:
        msg = f'Element not found, element: "{element}"'
        raise NoSuchElementException(msg)


def assert_visible_el(driver, element):
    with allure.step(f'Проверить видимость элемента: {element}'):
        try:
            wait_element(driver, element)
        except TimeoutException:
            f'Not found {element}'
        assert element_visible(driver, element), \
            f'Not found {element}'


def wait_element_with_try(driver, element):
    try:
        WebDriverWait(driver, TIME).until(EC.visibility_of_element_located(element))
    except TimeoutException:
        pass


def swipe_up(driver, element, swipe=True, from_the_middle=False):
    windows_size = driver.get_window_size()
    count = 0
    start_the_point = windows_size['height'] - 300
    if from_the_middle:
        start_the_point = windows_size['height'] / 2
    while count < 10 and not element_visible(driver, element) and swipe:
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(200, start_the_point)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(200, 52)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        count += 1


def swipe_down(driver, element):
    count = 0
    while count < 5 and not element_visible(driver, element):
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(200, 130)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(200, 700)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        count += 1


def tap_to_coordinate(driver, x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def swipe_up_without_el_visible(driver):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(200, 700)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(200, 130)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


@allure.step('Кликаем по клавиатуре')
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
    except NoSuchElementException:
        return False


def elements_presenter(driver, element) -> bool:
    return bool(len(driver.find_elements(*element)))


@allure.step('Кликаем по координатам')
def tap_to_offer(driver, x, y):
    loc_x = int(x) + 139
    lox_y = int(y) + 72
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(loc_x, lox_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


@allure.step('Кликаем по координатам')
def tap_to_offer_master_pass(driver, x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


@allure.step('Кликаем по координатам')
def tap_to_tech_support(driver, x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def press_key(driver, key):
    driver.press_keycode(key)


def get_location(driver, element):
    return driver.find_element(*element).location


def get_email():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + '@test.ru'


def close_app(driver):
    driver.press_keycode(187)
    TouchAction(driver).press(x=519, y=1309).wait(1000).move_to(x=472, y=22).release().perform()
    TouchAction(driver).press(x=599, y=1437).wait(1000).move_to(x=650, y=194).release().perform()


def grab_phone(driver, element):
    text_with_phone = get_text(driver, element)
    return ''.join([n for n in text_with_phone[text_with_phone.find("+"):] if n.isdigit()])


@allure.step('Перезагрузка приложения')
def restart_app(driver):
    app_id = None
    if tools.is_android(PLATFORM_NAME):
        app_id = driver.session['appPackage']
    if tools.is_ios(PLATFORM_NAME):
        app_id = driver.session['bundleId']
    if app_id is None:
        logging.error("Not found appPackage[ANDROID] or bundleId[IOS]")
    driver.terminate_app(app_id)
    driver.activate_app(app_id)


@allure.step('Подготовка к старту')
def prepare_for_start(restart, driver):
    if restart:
        restart_app(driver)


@allure.step(f'Выбор платформы {PLATFORM_NAME}')
def select_element(ios, android):
    if PLATFORM_NAME == "android":
        return android
    if PLATFORM_NAME == "ios":
        return ios


def clear_field(driver, element):
    driver.find_element(*element).clear()


def compare_text(text1, text2) -> bool:
    assert text1 == text2, f"EXP - {text1}, REAL - {text2}"
