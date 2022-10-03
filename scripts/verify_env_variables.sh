#!/bin/bash
red='\033[0;31m'
green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'

echo -e "${orange}Verifying environment variables..."

[[ $PLATFORM_NAME == 'android' || $PLATFORM_NAME == 'ios' ]] && echo -e "${green}PLATFORM_NAME = $PLATFORM_NAME ${nc}" || 
{ echo -e "${red}PLATFORM_NAME must be equal 'android' or 'ios', set it in tox.ini ${nc}"; exit 1; }

[[ -n $DEVICE_NAME ]] && echo -e "${green}DEVICE_NAME = $DEVICE_NAME ${nc}" || 
{ echo -e "${red}Set DEVICE_NAME in tox.ini ${nc}"; exit 1; }

if [[ $1 == 'alt' ]] ; then
    [[ $APPIUM_PORT =~ ^[0-9]+([.][0-9]+)?$ ]] && echo -e "${green}APPIUM_PORT = $APPIUM_PORT ${nc}" || 
    { echo -e "${red}Set Appium Port in tox.ini ${nc}"; exit 1; }
#
#    [[ -n $UDID ]] && echo -e "${green}UDID = $UDID ${nc}" ||
#    { echo -e "${red}Set Device UDID in tox.ini ${nc}"; exit 1; }
fi

echo -e "${orange}Environment variables verified successfully${nc}"