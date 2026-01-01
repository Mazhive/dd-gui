dd_gui (C++ Edition) Linux dd frontend
Een snelle, native Linux GUI voor het dd commando, geschreven in C++ met het Qt6 framework. Deze applicatie is speciaal ontworpen voor Debian 13 (Trixie) om veilig schijfkopieën te maken en te herstellen.

🚀 Kenmerken
Native Snelheid: Gecompileerd als een binary voor minimale overhead.

Real-time Monitoring: Volg de voortgang via een dynamische voortgangsbalk die van kleur verandert:

🔴 0-33%: Startfase

🟠 33-66%: Halverwege

🟢 66-100%: Bijna klaar

Instelbare Blokgrootte: Kies tussen 64K, 1M of 4M voor optimale prestaties op MicroSD-kaarten en SSD's.

Logvenster: Toont de volledige terminal output van dd in een ingebouwde console.

Veiligheid: Gebruikt stdbuf en conv=fsync om ervoor te zorgen dat data daadwerkelijk naar de schijf is geschreven voordat het proces als 'klaar' wordt gemarkeerd.

📦 Benodigdheden (Debian 13)
Om de broncode te compileren, heb je de volgende pakketten nodig:

Bash

sudo apt update
sudo apt install build-essential cmake qt6-base-dev libgl1-mesa-dev util-linux coreutils sudo
🛠️ Compileren en Installeren
Volg deze stappen om de executable te bouwen vanuit de src map:

Navigeer naar de projectmap:

Bash

cd ~/dd-gui
Maak een build-map aan en ga erin:

Bash

mkdir build && cd build
Configureer het project met CMake:

Bash

cmake ..
Compileer de code:

Bash

make
Start de applicatie:

Bash

./dd_gui
📖 Gebruik
Selecteer Bron: Kies een schijf uit de lijst of blader naar een .img bestand.

Selecteer Doel: Kies de doelschijf (bijv. je MicroSD-kaart). Let op: alle data op het doel wordt gewist!

Kies Snelheid: Selecteer 1M of 4M voor de beste resultaten op SD-kaarten.

Start: Klik op 'START CLONEN'. Voer je wachtwoord in wanneer de sudo prompt verschijnt.

dd_gui.desktop gebruikers kunnen dit bestand in hun eigen ~/.local/share/applications/ plaatsen

⚠️ Belangrijke Opmerking
De applicatie roept dd aan via sudo. Het is aanbevolen om de applicatie te starten vanuit de terminal of ervoor te zorgen dat je sudo geconfigureerd is om wachtwoorden via de GUI te accepteren (bijv. via pkexec).

## 🛠️ Snelle Installatie

Voer het volgende commando uit in je terminal om de app automatisch te compileren en toe te voegen aan je startmenu:

```bash
chmod +x install.sh && ./install.sh
