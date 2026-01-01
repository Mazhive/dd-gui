#!/bin/bash

# Kleuren voor output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Stap 1: Controleren van dependencies...${NC}"
sudo apt update
sudo apt install -y build-essential cmake qt6-base-dev libgl1-mesa-dev util-linux coreutils

echo -e "${GREEN}Stap 2: Compileren van dd_gui...${NC}"
mkdir -p build
cd build
cmake ..
make

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Compilatie geslaagd!${NC}"
else
    echo -e "${RED}Compilatie mislukt. Controleer de foutmeldingen hierboven.${NC}"
    exit 1
fi

echo -e "${GREEN}Stap 3: .desktop bestand configureren...${NC}"
# Bepaal het absolute pad van de executable
APP_PATH=$(pwd)/dd_gui
DESKTOP_FILE="$HOME/.local/share/applications/dd_gui.desktop"

# Schrijf het .desktop bestand met het juiste pad
cat <<EOF > $DESKTOP_FILE
[Desktop Entry]
Type=Application
Version=1.0
Name=DD GUI
Comment=Veilig schijven clonen en images schrijven
Exec=sudo $APP_PATH
Icon=drive-harddisk
Terminal=true
Categories=System;Utility;
Keywords=dd;clone;backup;usb;
EOF

chmod +x $DESKTOP_FILE

echo -e "${GREEN}--------------------------------------------------${NC}"
echo -e "${GREEN}Installatie voltooid!${NC}"
echo -e "Je kunt 'DD GUI' nu vinden in je applicatiemenu."
echo -e "LET OP: Omdat dd sudo-rechten nodig heeft, opent er een terminal"
echo -e "voor je wachtwoord wanneer je de app start."
echo -e "${GREEN}--------------------------------------------------${NC}"
