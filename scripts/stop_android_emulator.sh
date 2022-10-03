#!/bin/bash
red='\033[0;31m'
green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'

sleep 10
path_log=$(realpath ../logs)
rm -rf "$path_log"
mkdir "$path_log"
[[ -z "$UDID" ]] && UDID="emulator-5554"
"$HOME"/Library/Android/sdk/platform-tools/adb -s "$UDID" emu kill 2>&1 >> "$path_log"/android_emulator.log
echo "Stopping android emulator...successfully"