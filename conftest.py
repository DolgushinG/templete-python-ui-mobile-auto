import base64
import logging
import os
import random
import time
import warnings
import requests
import selenium

import manage_emul
import allure
from appium import webdriver as AppiumDriver
from appium.webdriver.appium_service import AppiumService
import pytest
from selenium.common import InvalidSessionIdException, WebDriverException

import tools
from config.options import get_options
from constants import OUTPUT_ROOT, LOGS_ROOT, SCREENSHOT_ROOT

PLATFORM_NAME = None or os.getenv('PLATFORM_NAME')
DEVICE_NAME = None or os.getenv('DEVICE_NAME')
ENV = None
SUITE = None
HOST = os.getenv('APPIUM_HOST') or '0.0.0.0'
PORT = os.getenv('APPIUM_PORT') or '4723'
WDA_PORT = os.getenv('WDA_PORT') or '8100'
BOOTSTRAP_PORT = os.getenv('BOOTSTRAP_PORT') or '4724'
APPIUM_URL = f'http://{HOST}:{PORT}/wd/hub'
logging.getLogger().setLevel(logging.INFO)


@pytest.fixture(scope="package", autouse=True)
def log():
    global DEVICE_NAME
    options = get_options(PLATFORM_NAME)
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"Testing app: {options.get_capability('app')}")
    logging.info(f"Platform: {options.get_capability('platformName')}")
    logging.info(f"Version: {options.get_capability('platformVersion')}")
    logging.info(f"wda: {WDA_PORT}")
    logging.info(f"Device name: {options.get_capability('deviceName')}")
    logging.info(f"Udid: {options.get_capability('udid')}")
    logging.info(f"Bootstrap port: {BOOTSTRAP_PORT}")
    logging.info(f"Appium url: http://{HOST}:{PORT}/wd/hub")
    logging.info(f"Env: {ENV.upper()}")
    DEVICE_NAME = options.get_capability('deviceName')


@pytest.fixture(scope="session", autouse=True)
def setup():
    logging.getLogger().setLevel(logging.ERROR)
    tools.prepare_adb(PLATFORM_NAME)
    appium_service = AppiumService()
    appium_service.start(
        args=[
            '-a', HOST, '-p', PORT, '-pa', '/wd/hub', '--log',
            f'{LOGS_ROOT}/appium.log', '--webdriveragent-port',
            WDA_PORT, '-bp', BOOTSTRAP_PORT]
    )
    if appium_service.is_running:
        logging.info(f"Running appium successfully")
    else:
        logging.error("Appium server doesn't running")
    manage_emul.start_platform(PLATFORM_NAME)
    tools.uninstall_sdk(PLATFORM_NAME)
    yield
    appium_service.stop()
    # manage_emul.stop_platform(PLATFORM_NAME)
    if appium_service.is_running:
        logging.error(f"Appium is still running")
    else:
        logging.info("Appium server stopped successfully")
    tools.adb_uninstall(PLATFORM_NAME)


@pytest.fixture(scope="function", autouse=True)
def driver(request, setup):
    options = get_options(PLATFORM_NAME)
    request.cls.driver = AppiumDriver.Remote(APPIUM_URL, options=options)
    yield request.cls.driver
    request.cls.driver.quit()
    try:
        request.cls.driver.session.values()
    except InvalidSessionIdException and WebDriverException:
        logging.info(msg="Status driver - quit driver")


def pytest_collection_modifyitems(items):
    tools.remove_test_dir(OUTPUT_ROOT)
    tools.remove_test_dir(f'{SCREENSHOT_ROOT}/{PLATFORM_NAME}/new/{DEVICE_NAME}')
    tools.remove_test_dir(f'{SCREENSHOT_ROOT}/{PLATFORM_NAME}/result/{DEVICE_NAME}')
    tools.remove_test_dir(f'{SCREENSHOT_ROOT}/{PLATFORM_NAME}/changes/{DEVICE_NAME}')
    # is_get_rid_available()
    global SUITE
    smoke_tests = smoke_suite()
    try:
        if "smoke" in items[0].config.invocation_params.args:
            logging.info(msg=f'SMOKE SUITE: {smoke_tests}')

    except IndexError:
        pass
    count_test = 0
    for item in items:
        item.add_marker(allure.label('PLATFORM_NAME', f'{PLATFORM_NAME}'.upper()))
        item.add_marker(allure.label('DEVICE_NAME', f'{DEVICE_NAME}'.upper()))
        if item.name in smoke_tests:
            count_test += 1
            item.add_marker(pytest.mark.smoke)
        else:
            count_test += 1
            item.add_marker(pytest.mark.full_without_smoke)
        SUITE = f'{count_test} TESTS'


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if not os.path.exists(f"{OUTPUT_ROOT}/text_fail.txt"):
            os.system(f'touch {OUTPUT_ROOT}/text_fail.txt')
        mode = "a" if os.path.exists(f"{OUTPUT_ROOT}/text_fail.txt") else "w"
        with open(f"{OUTPUT_ROOT}/text_fail.txt", mode) as f:
            f.write(rep.longreprtext + "\n")
    # if rep.when == 'call':
    #     item.session.results[item] = rep
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_run_record(request):
    try:
        request.cls.driver.start_recording_screen(timeLimit=1200, videoType="h264", videoQuality="low", bitRate=1000000)
    except InvalidSessionIdException as e:
        logging.error(msg=f'Something has gone wrong - {e}')


def pytest_configure(config):
    global PLATFORM_NAME
    global ENV
    PLATFORM_NAME = os.getenv('PLATFORM_NAME') or config.getoption("--platform")
    ENV = config.getoption("--env")


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addoption('--env', action='store', default="stage", help="Choose env: demo, stage, prod")
    parser.addoption('--platform', default="android", action='store', help="Choose app: android or ios")


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    if request.node.rep_call.failed:
        # Make the  video and screenshot if test failed:
        try:
            video_rawdata = request.cls.driver.stop_recording_screen()
            current_time = time.strftime("%Y_%m_%d_%H%M%S")
            name = request.function.__name__ + "_" + current_time
            video_name = "video_" + name
            img_name = "img_" + name
            filepath = f"{OUTPUT_ROOT}/{DEVICE_NAME}_{video_name}.mp4"
            with open(filepath, "wb+") as vd:
                vd.write(base64.b64decode(video_rawdata))
            allure.attach(open(filepath, "rb").read(),
                          name=video_name,
                          attachment_type=allure.attachment_type.MP4)
            allure.attach(request.cls.driver.get_screenshot_as_png(),
                          name=img_name,
                          attachment_type=allure.attachment_type.PNG)
        except:
            pass  # just ignore
    else:
        request.cls.driver.stop_recording_screen()


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, config):
    yield
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    tools.send_report_telegram_bot(terminalreporter, ENV, PLATFORM_NAME, SUITE)


def smoke_suite() -> list:
    main_smoke_suite = [
        "test_fill",
    ]
    return main_smoke_suite
