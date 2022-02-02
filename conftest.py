import base64
import os
import time
from datetime import datetime

import pytest
from appium import webdriver

from config.desired_capabilities import ANDROID
from config.desired_capabilities import IOS

APP = None
DEVICE = None
DRIVER = None
TEST_RAIL_RUN_ID = None


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
    appium_service = AppiumService()
    appium_service.start()
    time.sleep(2)
    emulator = {"ios": "ios_emul.py", "android": "android_emul.py"}
    subprocess.run(["python3", emulator[APP]])
    time.sleep(2)
    platform = {"ios": IOS, "android": ANDROID}
    request.cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_capabilities=platform[APP])
    request.cls.driver.start_recording_screen(timeLimit=1200, videoType="h264", videoQuality="high")
    yield
    request.cls.driver.quit()
    appium_service.stop()
    close_simulator(APP)


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


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
            video_raw_data = driver.stop_recording_screen()
            take_record_video(request, video_raw_data)
            print("executing test failed", request.node.nodeid)


def take_record_video(request, video_rawdata):
    video_name = f'{request.fspath.purebasename}_{time.strftime("%Y_%m_%d_%H%M%S")}'
    path_save = os.path.abspath("tests/output")
    filepath = os.path.join(path_save, video_name + "_" + APP + ".mov")
    with open(filepath, "wb+") as vd:
        vd.write(base64.b64decode(video_rawdata))

def pytest_collection_modifyitems(items):
    for item in items:
        # тест это словарь с марками testrail
        #{ANDROID = {"test_fill": "C19322",}
        if APP == "ПЛАТФОРМА":
            tests = TEST
        else:
            tests = TEST
        for testname in tests:
            if item.originalname == testname:
                item.add_marker(pytestrail.case(tests[testname]))

def close_simulator(emulator):
    if emulator == "android":
        os.system('adb emu kill')
    else:
        os.system('killall Simulator')