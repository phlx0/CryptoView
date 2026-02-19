#!/bin/bash

PURPLE="\033[0;35m"
CYAN="\033[0;36m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

echo -e "${PURPLE}"
echo "_________                        __            _____                 "
echo "\_   ___ \_______ ___.__._______/  |_  ____   /  _  \ ______ ______  "
echo "/    \  \/\_  __ <   |  |\____ \   __\/  _ \ /  /_\  \\____ \\____ \ "
echo "\     \____|  | \/\___  ||  |_> >  | (  <_> )    |    \  |_> >  |_> >"
echo " \______  /|__|   / ____||   __/|__|  \____/\____|__  /   __/|   __/ "
echo "        \/        \/     |__|                       \/|__|   |__|    "
echo -e "${RESET}"

echo -e "${CYAN}Initializing CryptoApp setup...${RESET}"

if [ ! -d "venv" ]; then
    echo -ne "${GREEN}Creating virtual environment...${RESET}"
    python3 -m venv venv &
    spinner $!
    echo -e " ${CYAN}[Virtual enviroment created!]${RESET}"
else
    echo -e "${YELLOW}Virtual environment already exists.${RESET}"
fi

echo -e "${CYAN}Activating virtual environment...${RESET}"
source venv/bin/activate

echo -ne "${GREEN}Upgrading pip...${RESET}"
pip install --upgrade pip &> /dev/null &
spinner $!
echo -e " ${CYAN}[DONE]${RESET}"

echo -ne "${PURPLE}Installing Python dependencies...${RESET}"
pip install -r requirements.txt &> /dev/null &
spinner $!
echo -e " ${CYAN}[COMPLETED]${RESET}"

echo -e "${PURPLE}"
echo "CryptoApp is ready! 💜"
echo -e "${RESET}"
echo "============================================================="
echo -e "${CYAN}Run the app with:${RESET} source venv/bin/activate && python3 main.py"
echo "============================================================="