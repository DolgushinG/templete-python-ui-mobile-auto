#!/usr/bin/env python3

import os
import subprocess
import time
from pathlib import Path


def start_emul(app):
    time.sleep(1)
    if app == "android":
        android_emulator_dir: Path = Path(os.environ['ANDROID_HOME'] or os.environ['ANDROID_SDK']) / 'emulator'

        if android_emulator_dir.exists():
            emulator_dir = android_emulator_dir.absolute()
            print(f'SDK emulator dir: {emulator_dir}', end='\n\n')

            proc = subprocess.Popen(['./emulator', '-list-avds'], stdout=subprocess.PIPE, cwd=emulator_dir, text=True)
            avds = {idx: avd_name.strip() for idx, avd_name in enumerate(proc.stdout, start=1)}

            print('\n'.join([f'{idx}: {avd_name}' for idx, avd_name in avds.items()]))

            # avd_idx = input("\nType AVD index and press Enter... ")
            avd_idx = 1
            avd_name = avds.get(int(avd_idx))

            if avd_name:
                subprocess.Popen(['./emulator', '-avd', avd_name, '-no-boot-anim'], cwd=emulator_dir)
                time.sleep(2)
            else:
                print('Invalid AVD index')
        else:
            print(f'Either $ANDROID_HOME or $ANDROID_SDK must be defined!')
    else:
        running_ios = os.popen('xcrun simctl bootstatus booted -b').read()
        if not running_ios:
            os.system('open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app')
            time.sleep(1)
        else:
            print("ios already RUNNING")