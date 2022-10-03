#!/bin/bash
red='\033[0;31m'
green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'

echo "Stopping ios simulator..."
path_log=$(realpath ../logs)
[[ -z "$UDID" ]] && echo "UDID has not found"
xcrun simctl shutdown "$UDID" 2>&1 >> "$path_log"/ios_simulator.log
xcrun simctl erase "$UDID" 2>&1 >> "$path_log"/ios_simulator.log
echo "Stopping ios simulator...successfully"
