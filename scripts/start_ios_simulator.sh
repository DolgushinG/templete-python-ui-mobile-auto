#!/bin/bash
red='\033[0;31m'
green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'


echo "Starting ios simulator..."
path_log=$(realpath ../logs)
rm -rf "$path_log" || true
mkdir "$path_log" || true
[[ -z "$UDID" ]] && echo "UDID has not found"
xcrun simctl bootstatus "$UDID" -b 1>"$path_log"/ios_simulator.log