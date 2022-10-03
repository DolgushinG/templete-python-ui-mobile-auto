import logging
import os
import time

import allure
import tools
from conftest import PLATFORM_NAME, ENV, DEVICE_NAME
from constants import PROJECT_ROOT


class BasePage:
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.driver = driver
        self.platform_name = PLATFORM_NAME
        self.device_name = DEVICE_NAME
        self.env = ENV

    current_time = time.strftime("%Y_%m_%d_%H%M%S")

    def take_screenshot(self, screenshot_name):
        directory_new = f'{PROJECT_ROOT}/screenshots/{self.platform_name}/new/{self.device_name}'
        self.check_exist_dir(directory_new)
        path = f'{directory_new}/{screenshot_name}_{self.current_time}.png'
        self.driver.save_screenshot(path)

        tools.crop_status_bar(path, self.platform_name)

    def check_exist_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def compare_image(self, org, new):
        directory_org = f'{PROJECT_ROOT}/screenshots/{self.platform_name}/org/{self.device_name}'
        directory_new = f'{PROJECT_ROOT}/screenshots/{self.platform_name}/new/{self.device_name}'
        directory_changes = f'{PROJECT_ROOT}/screenshots/{self.platform_name}/changes/{self.device_name}'
        directory_result = f'{PROJECT_ROOT}/screenshots/{self.platform_name}/result/{self.device_name}'
        self.check_exist_dir(directory_org)
        self.check_exist_dir(directory_new)
        self.check_exist_dir(directory_changes)
        self.check_exist_dir(directory_result)

        if os.path.exists(f'{directory_org}/{org}.png'):
            original_path = f'{directory_org}/{org}.png'
            copy_original_path = f'{directory_org}/{org}_copy.png'
            new_path = f'{directory_new}/{new}_{self.current_time}.png'
            changes_path = f'{directory_changes}/{org}_changes_{self.current_time}.png'
            result_path = f'{directory_result}/{org}_diff_comb_{self.current_time}.png'
            is_same = tools.compare(driver=self.driver, platform=self.platform_name, device_name=self.device_name, img1=original_path, img2=new_path,
                                    changes_path=changes_path)
            if not is_same:
                tools.draw_text('new', new_path)
                tools.draw_text('original', original_path, copy_original_path)
                tools.draw_text('changes', changes_path)
                tools.combine_image(img1=new_path, img2=copy_original_path, img3=changes_path, result_path=result_path)
                allure.attach.file(result_path, name="result_changes_screenshot",
                                   attachment_type=allure.attachment_type.PNG)
                os.remove(copy_original_path)
            with allure.step('Проверка стартовой страницы визуально'):
                assert is_same, f'Скриншоты различаются - разница будет показана на картинке {result_path}'
        else:
            path = f'{directory_org}/{org}.png'
            self.driver.save_screenshot(path)
            tools.crop_status_bar(path, self.platform_name)
