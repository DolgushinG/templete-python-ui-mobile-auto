import base64
import os
from pathlib import Path

from constants import OUTPUT_ROOT


def close_simulator(simulator):
    if simulator == "android":
        os.system('adb emu kill')
    else:
        os.system('killall Simulator')


def take_record_video(request, video_rawdata):
    video_name = f'{request.node.name}'
    Path(OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(OUTPUT_ROOT, video_name + ".mov")
    with open(filepath, "wb+") as vd:
        vd.write(base64.b64decode(video_rawdata))


def remove_test_dir():
    Path(OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)
    if os.path.isdir(OUTPUT_ROOT):
        for f in os.listdir(OUTPUT_ROOT):
            if not f.endswith(".mov"):
                continue
            os.remove(os.path.join(OUTPUT_ROOT, f))
