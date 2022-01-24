import pytest

from config.desired_capabilities import ANDROID, BROWSERSTACK, BROWSERSTACK_IOS
from config.desired_capabilities import IOS
from appium import webdriver
import sys

APP = None
DEVICE = None
DRIVER = None


def pytest_configure(config):
    global APP
    global DEVICE
    APP = config.getoption("--app")
    DEVICE = config.getoption("--device")


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addoption('--app', action='store', default="android", help="Choose App: ios or android")
    parser.addoption('--device', action='store', default="emulator", help="Choose Device: simulator / emulator / real "
                                                                          "device")
    parser.addoption('--reset', action='store', default="false", help="Reset app true and false")


@pytest.fixture(scope="class")
def driver(request):
    platform = {"ios": IOS, "android": ANDROID, "browserstack": BROWSERSTACK, "browserstack_ios": BROWSERSTACK_IOS}

    if DEVICE == "browserstack":
        if APP == "ios":
            request.cls.driver = webdriver.Remote("http://hub-cloud.browserstack.com/wd/hub",
                                                       platform["browserstack_ios"])
        else:
            request.cls.driver = webdriver.Remote("http://hub-cloud.browserstack.com/wd/hub",
                                                       platform["browserstack"])
    else:
        request.cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", platform[APP])
        if APP == "android":
            request.cls.driver.hide_keyboard()
    yield
    if APP == "android":
        request.cls.driver.hide_keyboard()
    request.cls.driver.quit()

