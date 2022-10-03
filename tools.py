import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path
import time
import cv2
import imutils
import requests
from appium.webdriver.common.appiumby import AppiumBy
from subprocess import Popen, PIPE
from PIL import Image, ImageFont, ImageDraw

from constants import OUTPUT_ROOT


def set_type_selector(element: str) -> tuple:
    if '//' in element:
        return AppiumBy.XPATH, element
    if '**/' in element:
        return AppiumBy.IOS_CLASS_CHAIN, element
    if '==' in element:
        return AppiumBy.IOS_PREDICATE, element
    if ':id' in element:
        return AppiumBy.ID, element
    return AppiumBy.NAME, element


def crop_status_bar(img, platform):
    in_file = img
    out_file = img
    img = Image.open(in_file)
    width, height = img.size
    # crop
    # 10 pixels from the left
    # 20 pixels from the top
    # 30 pixels from the right
    # 40 pixels from the bottom
    if is_android(platform):
        cropped = img.crop((0, 90, width - 0, height - 90))
    else:
        cropped = img.crop((0, 90, width - 0, height - 0))
    cropped.save(f"{out_file}")


def combine_image(img1, img2, img3, result_path):
    images = [Image.open(x) for x in [img1, img2, img3]]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.save(result_path)


def draw_text(text, path, save_path=None):
    img = Image.open(path)
    font = ImageFont.truetype("/System/Library/Fonts/Keyboard.ttf", 130)
    I1 = ImageDraw.Draw(img)
    I1.text(xy=(158, 156), text=text, fill=(255, 0, 0), font=font)
    img.save(save_path or path)


def compare(driver, platform, device_name, img1, img2, changes_path):
    if is_android(platform):
        height = 2210
    if is_ios(platform):
        window_size = driver.get_window_size()
        height = window_size['height']
    original = cv2.imread(img1)
    new = cv2.imread(img2)
    original = imutils.resize(original, height=height)
    new = imutils.resize(new, height=height)
    diff = original.copy()
    cv2.absdiff(original, new, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if cnts:
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(changes_path, new)
        return False
    else:
        return True


def remove_test_dir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    if os.path.isdir(dir_path):
        for f in os.listdir(dir_path):
            if not f.endswith(".mp4") and not f.endswith(".png") and not f.endswith(".txt"):
                continue
            else:
                try:
                    os.remove(os.path.join(dir_path, f))
                except FileNotFoundError:
                    pass


def prepare_adb(app):
    if is_android(app):
        udid = os.getenv("UDID")
        os.system(f'$ANDROID_HOME/platform-tools/adb -s {udid} forward --remove-all > /dev/null 2>&1')


def get_booted_udid_ios():
    devices = os.popen(f"xcrun simctl list 'devices' '{os.getenv('DEVICE_NAME') or 'iPhone 11'}' --json").read().strip()
    devices_udid = {}
    platform_version = os.getenv("PLATFORM_VERSION") or "15.5"
    devices = json.loads(devices)['devices'][f'com.apple.CoreSimulator.SimRuntime.iOS-{platform_version.replace(".", "-") or "15-5"}']
    for device in devices:
        devices_udid[device['name']] = device['udid']
    return devices_udid


def get_booted_udid_android():
    devices = []
    with Popen(['$HOME/Library/Android/sdk/platform-tools/adb devices'], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines()[1:-1]:
            devices.append(val.decode('UTF-8').replace('device', '').strip())
    emulator = []
    with Popen(['$HOME/Library/Android/sdk/emulator/emulator -list-avds'], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines():
            emulator.append(val.decode('UTF-8').replace('/n', '').strip().replace(" ", ''))
    udid_and_name = {}
    for x in range(len(devices)):
        udid_and_name[emulator[x]] = devices[x]
    return udid_and_name


def adb_uninstall(app):
    if is_android(app):
        udid = os.getenv("UDID")
        os.system(f'$ANDROID_HOME/platform-tools/adb -s {udid} forward --remove-all > /dev/null 2>&1')
        os.system('$ANDROID_HOME/platform-tools/adb uninstall io.appium.settings > /dev/null 2>&1')
        os.system('$ANDROID_HOME/platform-tools/adb uninstall io.appium.unlock > /dev/null 2>&1')
        os.system('$ANDROID_HOME/platform-tools/adb uninstall io.appium.uiautomator2.server > /dev/null 2>&1')
        os.system('$ANDROID_HOME/platform-tools/adb uninstall io.appium.uiautomator2.server.test > /dev/null 2>&1')


def is_mobile_user() -> bool:
    user = str(os.popen("whoami").read()).strip()
    if user == "mobile":
        return True
    else:
        return False


def is_android(platform):
    return platform == 'android'


def is_ios(platform):
    return platform == 'ios'


def is_stage(env):
    return env == 'stage'


def is_demo(env):
    return env == 'demo'


def remove_space_and_new_line(text) -> str:
    if " " in text or "\n" in text:
        return text.replace(" ", " ").replace("\n", " ")
    return text.strip()


def convert_str_to_num_or_float(text):
    try:
        return int(text)
    except ValueError:
        return float(text.replace(",", "."))


def remove_mask_phone(phone: str) -> str:
    return phone.replace("+", "").replace("(", "").replace(")", "").replace(" ", "").replace("-", "")


def remove_space_from_number(number: int) -> str:
    return "{:,.2f}".format(number).replace(",", "X").replace(".", ",").replace("X", ".").replace(".", " ")


def send_report_telegram_bot(terminalreporter, env, app, suite):
    failed = len(terminalreporter.stats.get('failed', []))
    passed = len(terminalreporter.stats.get('passed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    error = len(terminalreporter.stats.get('error', []))
    xfailed = len(terminalreporter.stats.get("xfailed", []))
    xpassed = len(terminalreporter.stats.get("xpassed", []))

    token = ""
    telegram_uri = f'https://api.telegram.org/bot{token}'
    chat_id = ""

    success_sticker_id = "CAACAgIAAxkBAAEXQYVi_3DzKogIpEiH_UnMoDI1LS1wbAACFAADsND4DDQYKpXU6o9pKQQ"
    fail_sticker_id = "CAACAgIAAxkBAAEXQYdi_3EyrMDcBtw-fZdiTDwVITbLKgACIwADsND4DGmmygHGlyggKQQ"
    report_url = ""
    disable_stickers = True
    list_failed = 1
    list_failed_amount = 3

    failed_tests = ''
    error_tests = ''
    if list_failed and failed != 0:
        failed_tests = '\nFailed tests:\n'

        for failed_test in terminalreporter.stats.get('failed', [])[:list_failed_amount]:
            failed_tests += f'{failed_test.nodeid}\n'

        if failed > list_failed_amount:
            failed_tests += '...'
    if list_failed and error != 0:
        error_tests = '\nError tests:\n'

        for error_test in terminalreporter.stats.get('error', [])[:list_failed_amount]:
            error_tests += f'{error_test.nodeid}\n'

        if error > list_failed_amount:
            error_tests += '...'
    final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s' % (
        passed, failed, skipped, error, xfailed, xpassed)

    session_time = time.time() - terminalreporter._sessionstarttime
    time_taken = f'\nTime taken: {str(time.strftime("%H:%M:%S", time.gmtime(session_time)))}'

    if failed == 0 and error == 0:
        sticker_payload = {'chat_id': chat_id, 'sticker': success_sticker_id}
    else:
        sticker_payload = {'chat_id': chat_id, 'sticker': fail_sticker_id}
    message_id = None
    success_emoji = "✅"
    failed_emoji = "❌"
    emoji = success_emoji if not failed and not error else failed_emoji
    if not disable_stickers:
        message_id = requests.post(f'{telegram_uri}/sendSticker', json=sticker_payload, verify=False).json()['result'][
            'message_id']
    message_payload = {'chat_id': chat_id,
                       'text': f'\n{emoji} \n '
                               f'Current Date - {datetime.today().strftime("%Y-%m-%d %H:%M:%S")} \n '
                               f'User - {str(os.popen("whoami").read()).strip()} \n '
                               f'{final_results}{time_taken} \n '
                               f'{report_url} \n '
                               f'PLATFORM - {app.upper()} \n '
                               f'DEVICE - {os.getenv("DEVICE_NAME").upper()} \n '
                               f'SUITE - {suite} \n '
                               f'ENV - {env.upper()} \n '
                               f'{failed_tests} \n '
                               f'{error_tests} \n ',
                       'reply_to_message_id': message_id}
    requests.post(f'{telegram_uri}/sendMessage', json=message_payload, verify=False).json()
    if os.path.exists(f"{OUTPUT_ROOT}/text_fail.txt") and not failed == 0 and not error == 0:
        with open(f"{OUTPUT_ROOT}/text_fail.txt", "rb") as filetxt:
            title = "text_fail.txt"
            requests.post(f'{telegram_uri}/sendDocument', data={"chat_id": chat_id, "caption": title}, files={"document": filetxt}, verify=False).json()



def install_app(app, bank, udid):
    if is_android(app):
        os.system(f'$ANDROID_HOME/platform-tools/adb -s {udid} install {bank} > /dev/null 2>&1')
    if is_ios(app):
        os.system(f'xcrun simctl install {udid} {bank}')


def uninstall_app(app, bank, udid):
    if is_android(app):
        os.system(f'$ANDROID_HOME/platform-tools/adb -s {udid} uninstall {bank} > /dev/null 2>&1')
    if is_ios(app):
        os.system(f'xcrun simctl uninstall {udid} {bank}')
