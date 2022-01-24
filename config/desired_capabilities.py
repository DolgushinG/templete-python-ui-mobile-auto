'''
Get the desired capabilities to start the automation which include
1. platformName
2. platformVersion
3. deviceName :  On Android this capability is currently ignored, though it remains required.
4. app: app=PATH('../../apps/' + app)
    If you don't have apk of application then provide appPackage and appActivity
5. appPackage
6. appActivity
'''
import os
path_app_android = "/test.apk"
app_android = os.path.abspath("app") + path_app_android
ANDROID = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Emulator",
    "appium:appPackage": "",
    "appium:appWaitActivity": "",
    "appium:app": app_android,
    "autoGrantPermissions": "true",
    "appium:autoAcceptAlerts": "false",
    "appium:noReset": "true",
    # "appium:fullReset": "true",
}

IOS = {
    "platformName": "iOS",
    "appium:platformVersion": "15.2",
    "appium:deviceName": "iPhone 11",
    "appium:automationName": "XCUITest",
    "autoGrantPermissions": "true",
    "appium:autoAcceptAlerts": "true",
    "appium:noReset": "false",
    # "appium:fullReset": "true",
    "appium:app": os.path.abspath("test.app")
}
BROWSERSTACK = {
    # Set your access credentials
    "browserstack.user": "",
    "browserstack.key": "",
    "autoGrantPermissions": "true",
    "autoAcceptAlerts": "true",
    "noReset": "false",
    # Set URL of the application under test
    "app": "",

    # Specify device and os_version for testing
    "device": "Google Pixel 4",
    "os_version": "10.0",

    # Set other BrowserStack capabilities
    "project": "mobile_autotests",
    "build": "ANDROID",
    "name": "auth_tests"
}
BROWSERSTACK_IOS = {
    # Set your access credentials
    "browserstack.user": "",
    "browserstack.key": "",

    # Set URL of the application under test
    "app": "",

    # Specify device and os_version for testing
    "device": "iPhone 11 Pro",
    "os_version": "15",

    # Set other BrowserStack capabilities
    "project": "mobile_autotests_ios",
    "build": "IOS",
    "name": "auth_tests_ios"
}
