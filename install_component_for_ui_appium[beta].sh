#!/bin/zsh
red='\033[0;31m'
green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'



echo -e "${orange}Installing component for ui mobile auto APPIUM..."
echo -e "${green}================================================================================"
brew_status=$(brew -v)
echo -e "${orange}Checking installed brew..."
if [[ "$brew_status" =~ 'Homebrew' ]]; then
   echo -e "${green}Checked installed brew...ok"
else
    echo "Homebrew not installed and starting install"
    /bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
echo -e "${green}================================================================================"
echo -e "${orange}Checking installed node js..."
path_node=$(where node2)
if [[ "$path_node" =~ '/usr/local/' ]]; then
    echo -e "${red}Node installed not correct, please remove node, and restart install node in brew"
else
    if [[ "$path_node" =~ '/usr/local/' ]]; then
      echo "Node installed not correct, please remove node /usr/local/...., and restart install node in brew"
    fi
    if [[ "$path_node" =~ 'not found' ]] || [[ "$path_node" =~ 'homebrew' ]]  ; then
        if [[ "$path_node" =~ 'not found' ]]; then
          echo -e "${green}Node not installed or start install node and continue"
          brew install node
        fi
        echo -e "${green}================================================================================"
        echo -e "${orange}Installing appium-doctor..."
        npm install @appium/doctor --location=global &&
        echo -e "${green}================================================================================"
        echo -e "${orange}Installing appium ..."
        npm install -g appium &&
        echo -e "${green}================================================================================"
        echo -e "${orange}Installing applesimutils ..."
        brew tap wix/brew &&
        brew install applesimutils &&
        echo -e "${green}================================================================================"
        echo -e "${orange}Installing set-simulator-location ..."
        brew install lyft/formulae/set-simulator-location &&
        echo -e "${green}================================================================================"
        echo -e "${orange}Installing mjpeg-consumer ..."
        npm i -g mjpeg-consumer &&
        echo -e "${green}================================================================================"
        echo -e "${orange}Installing opencv4nodejs ..."
        npm i -g opencv4nodejs &&
        echo -e "${green}================================================================================"
        echo -e "${green}Appium component installed successfully${nc}"
    fi
fi

