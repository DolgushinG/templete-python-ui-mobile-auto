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

# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.cls.driver
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# make a screenshot with a name of the test, date and time
def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/", "_").replace("::", "__")
    driver.save_screenshot(f'output/{file_name}')