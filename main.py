
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from pages.PaymentPage import PaymentPage


TIME = 15


def fill_field(driver, element, text, clear=False):
    if clear:
        driver.find_element(*element).clear()
    driver.find_element(*element).send_keys(text)

def get_text(driver, element):
    return driver.find_element(*element).text

def get_attribute(driver, element, attribute):
    return driver.find_element(*element).get_attribute(attribute)

def wait_and_click(driver, element):
    WebDriverWait(driver, TIME).until(EC.element_to_be_clickable(element))
    driver.find_element(*element).click()

def wait_element(driver, element):
    WebDriverWait(driver, TIME).until(EC.presence_of_element_located(element))


def element_visible(driver, element):
    try:
        element = driver.find_element(*element)
        return element.is_displayed()
    except NoSuchElementException:
        return False


def ios_back_app(driver):
    TouchAction(driver).tap(x=59, y=39).perform()

def ios_swipe_up_to_down(driver):
    TouchAction(driver).press(x=198, y=83).wait(1000).move_to(x=184, y=798).release().perform()

def implicitly_wait(driver, time):
    driver.implicitly_wait(time)

def close_app(driver):
    driver.press_keycode(187)
    implicitly_wait(driver, 3)
    TouchAction(driver).press(x=519, y=1309).wait(1000).move_to(x=472, y=22).release().perform()
    implicitly_wait(driver, 3)
    TouchAction(driver).press(x=599, y=1437).wait(1000).move_to(x=650, y=194).release().perform()

def restart_app(driver):
    driver.close_app()
    driver.launch_app()
