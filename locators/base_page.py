from appium.webdriver.common.appiumby import AppiumBy

import tools
from main import select_element


class BasePageLocator:
    SELECT_SOME = select_element(
        ios=tools.set_type_selector('some'),
        android=tools.set_type_selector('some'))
