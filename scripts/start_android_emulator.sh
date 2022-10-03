#!/bin/bash
# shellcheck disable=SC2034
red='\033[0;31m'
green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'


echo "Starting android emulator..."
path_log=$(realpath ../logs)
rm -rf "$path_log"
mkdir "$path_log"
[[ -z "$DEVICE_NAME" ]] && DEVICE_NAME="Pixel_4_API_31" && echo -e "${orange}Device name not set and used default Pixel_4_API_31..."
[[ -z "$AVD_PORT" ]] && AVD_PORT="5554" && echo -e "${orange}PORT not set and used default 5554..."
"$HOME"/Library/Android/sdk/emulator/emulator -avd $DEVICE_NAME -port $AVD_PORT -delay-adb -no-boot-anim -wipe-data  1>"$path_log"/android_emulator.log 2>&1 &
gtimeout 30 "$HOME"/Library/Android/sdk/platform-tools/adb -s $DEVICE_NAME wait-for-device shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'
echo "Starting android emulator...successfully"


