Python DD Cloner (GUI)
Een gebruiksvriendelijke grafische interface voor het krachtige dd commando, speciaal geoptimaliseerd voor Debian 13 (Trixie). Met deze tool kun je veilig en eenvoudig schijven clonen, images maken en back-ups terugzetten zonder ingewikkelde commando's in de terminal te hoeven typen.

✨ Kenmerken
Pre-flight Dependency Check: Controleert bij het opstarten of alle benodigde systeemtools aanwezig zijn.

Visuele Progressie: Een voortgangsbalk die van kleur verandert (Rood 🔴 → Oranje 🟠 → Groen 🟢).

Instelbare Blokgrootte: Kies tussen 64K, 1M of 4M voor optimale snelheid.

Veiligheid: Ingebouwde bevestigingsvensters en een directe "STOP" knop om het proces af te breken.

Real-time Log: Volg de exacte output van het dd proces in het ingebouwde tekstvenster.

File Browser: Ondersteuning voor zowel fysieke schijven (/dev/sdX) als .img bestanden.

🛠️ Benodigdheden voor Debian 13
De applicatie maakt gebruik van standaard Linux-tools. Zorg ervoor dat de volgende pakketten zijn geïnstalleerd:

Bash

sudo apt update
sudo apt install python3 python3-tk util-linux coreutils 
sudo python3-tk: Voor de grafische interface.

util-linux: Voor lsblk (schijfdetectie).

coreutils: Voor het dd commando zelf.

🚀 Installatie & Gebruik
Clone de repository of download het script:

Bash

git clone https://github.com/Mazhive/dd-gui.git
cd dd-gui
Maak het script uitvoerbaar:

Bash

chmod +x dd_gui.py
Start de applicatie: Omdat dd directe toegang tot hardware vereist, is het aanbevolen de app met root-rechten te starten:

Bash

sudo python3 dd_gui.py
⚠️ Waarschuwing
Het gebruik van dd is krachtig maar riskant. Het overschrijven van de verkeerde schijf leidt tot onmiddellijk dataverlies. Controleer altijd dubbel of je de juiste Source (Bron) en Destination (Doel) hebt geselecteerd voordat je op Start klikt.

📸 Screenshots
(Tip: Voeg hier later een screenshot toe van je werkende app!)

📄 Licentie
Dit project is beschikbaar onder de MIT-licentie. Zie het LICENSE bestand voor details.
