import logging
import os
from typing import Any

import tools
from constants import APP_ROOT
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def get_platform_version():
    return str(os.popen("xcrun simctl getenv 'iPhone 11' SIMULATOR_RUNTIME_VERSION").read()).strip()


def get_app(platform_name):
    apps = os.listdir(APP_ROOT)
    app_filter = {
        'ios': 'app',
        'android': 'apk'
    }
    for app in apps:
        if app_filter[platform_name] in app:
            return f"{APP_ROOT}/{app}"
    logging.info(msg='Not found app, in dir apps {}'.format(apps))


def get_options(platform_name) -> Any:
    options = None
    if platform_name == 'android':
        options = UiAutomator2Options()
        default_device_name = 'Pixel_4_API_31'
        default_bootstrap_port = '4724'
        try:
            if os.getenv("UDID") is None:
                info_devices = tools.get_booted_udid_android()
                udid = info_devices[os.getenv('DEVICE_NAME') or default_device_name]
                options.set_capability('udid', udid)
            else:
                udid = os.getenv("UDID")
                options.set_capability('udid', udid)
        except KeyError:
            logging.info(msg=f"Not booted device {os.getenv('DEVICE_NAME')}")
        options.set_capability('app', get_app('android'))
        options.set_capability('autoGrantPermissions', 'true')
        options.set_capability('autoAcceptAlerts', 'false')
        options.set_capability('appPackage', '')
        options.set_capability('deviceName', os.getenv('DEVICE_NAME') or default_device_name)
        options.set_capability('platformVersion', "12")
        options.set_capability('bootstrapPort', os.getenv('BOOTSTRAP_PORT') or default_bootstrap_port)
    if platform_name == 'ios':
        options = XCUITestOptions()
        default_device_name = 'iPhone 11'
        default_wda_port = '8100'
        default_platform_version = '15.5'
        try:
            udid = tools.get_booted_udid_ios()[os.getenv('DEVICE_NAME') or default_device_name]
            options.set_capability('udid', udid)
        except KeyError:
            logging.info(msg=f"Not booted device {os.getenv('DEVICE_NAME')}")
        options.set_capability('platformVersion', f'{os.getenv("PLATFORM_VERSION") or default_platform_version}')
        options.set_capability('deviceName', os.getenv('DEVICE_NAME') or default_device_name)
        options.set_capability('app', get_app('ios'))
        options.set_capability('bundleId', "")
        options.set_capability('wdaLocalPort', int(os.getenv('WDA_PORT') or default_wda_port))
        options.set_capability("includeSafariInWebviews", True)
        options.set_capability("newCommandTimeout", 3600)
        options.set_capability("connectHardwareKeyboard", True)


    return options
