#!/usr/bin/env python3
import os
import time
from constants import PROJECT_ROOT


def start_platform(platform):
    time.sleep(1)
    if platform == "android":
        is_running_emulator = os.popen('$HOME/Library/Android/sdk/platform-tools/adb devices').read()
        if 'emulator' not in is_running_emulator:
            os.system(f'{PROJECT_ROOT}/scripts/start_android_emulator.sh')
    else:
        running_ios = os.popen('xcrun simctl bootstatus booted -b').read()
        if not running_ios:
            os.system(f'{PROJECT_ROOT}/scripts/start_ios_simulator.sh')


def stop_platform(platform):
    time.sleep(1)
    if platform == "android":
        os.system(f'{PROJECT_ROOT}/scripts/stop_android_emulator.sh')
    if platform == "ios":
        os.system(f'{PROJECT_ROOT}/scripts/stop_ios_simulator.sh')
