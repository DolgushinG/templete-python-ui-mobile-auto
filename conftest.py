import logging
import os

import pytest
import urllib3
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from config.desired_capabilities import platform
from start_emul import start_emul
from tools import take_record_video, remove_test_dir

APP = None
urllib3.disable_warnings()
appium_service = AppiumService()
logging.getLogger().setLevel(logging.INFO)


def pytest_configure(config):
    global APP
    APP = config.getoption("--app")


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addoption('--app', action='store', default="android", help="Choose App: ios or android")
    parser.addoption('--reset', action='store', default="0", help="Start with reset a simulator")


def add_new_params_for_start(request):
    args = request.config.invocation_params.args
    if '--reset' in args:
        platform[APP]['fullReset'] = True
    return platform[APP]


@pytest.fixture(scope="class")
def driver(request):
    config = add_new_params_for_start(request)
    reinstall_app()
    request.cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_capabilities=config)
    yield
    request.cls.driver.quit()


def start_service():
    appium_service.start()
    logging.info(msg='Appium is running? {}'.format(appium_service.is_running))
    logging.info(msg='Appium is listening? {}'.format(appium_service.is_listening))


def reinstall_app():
    if APP == 'android':
        os.system('$ANDROID_HOME/platform-tools/adb uninstall ru.test.app')
    if APP == 'ios':
        os.system('xcrun simctl uninstall booted org.test.demo.app')


@pytest.fixture(scope="session", autouse=True)
def setup():
    running = appium_service.is_running
    listening = appium_service.is_listening
    if running or listening is False:
        start_service()
    start_emul(APP)
    remove_test_dir()
    yield
    appium_service.stop()
    logging.info(msg='Appium is running? {}'.format(appium_service.is_running))
    logging.info(msg='Appium is listening? {}'.format(appium_service.is_listening))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_run_record(request):
    request.cls.driver.start_recording_screen(timeLimit=1200, videoType="h264", videoQuality="high")


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            video_raw_data = request.cls.driver.stop_recording_screen()
            take_record_video(request, video_raw_data)
            print("executing test failed", request.node.nodeid)
