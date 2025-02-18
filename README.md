# Test IoT Kafka

Ce repo contient le code pour une démonstration IoT avec fog computing.

## Cloud

La partie cloud est un stack docker qui contient le broker kafka ainsi que tous les composants permettant l'administration.

### Installation

 1. Assurez vous d'avoir installé docker et docker compose (docker desktop pour Windows) 
 2. Faites une copie du fichiez `.env` dans `.env.local`.
 3. Remplissez les informations dans le fichier `.env.local`. Attention vous ne devez pas mettre d'informations confidentielles dans le fichier `.env`.
 4. Naviguez vers le dossier `cloud` puis exécutez la commande `docker compose up -d`. Les images docker font plusieurs Go, il est normal que ce soit long.
 5. Si vous modifiez les variables d'environnement : `docker compose down` puis `docker compose up -d`
 6. Quelques secondes après que les containers aient démarrés, vous devriez pouvoir accéder au control center à l'adresse `http://localhost:9021`

## Fog

La partie fog est un Raspberry Pi qui sert de proxy entre mqtt et kafka.

### Installation

#### 1. OS
 1. Installez un système d'exploitation sur une carte sd (ex: Rasberry Pi OS Lite (64-bit)) avec un logiciel type Raspberry Pi Imager.
 2. Mettez à jour les paquets `sudo apt update && sudo apt upgrade -y`
#### 2. Installez docker
 1. retirez tous les paquets non compatibles : 
`for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done`
2. 
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
3. Installez docker : `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

#### 3. Proxy MQTT-Kafka

 1. Créez un fichiez `docker-compose.yml` (`nano docker-compose.yml` dans le terminal).
 2. Collez dans ce fichier le contenu du fichier `edge/docker-compose.yml`. Sauvegardez (Ctrl+x sur nano).
 3. `docker compose up -d`

## Edge

La partie Edge est un programme MicroPython exécuté sur une carte esp32.

### Installation

 1. Flashez le firmware MicroPython sur votre esp32 (cf: https://youtu.be/qoogOzSM0cM?si=lK63jA8VKgjrxdNt)
 2. Sauvegardez les fichiers `main.py`, `boot.py` et `wificredentials.py` sur votre esp32.
 3. Modifiez les paramètres wifi dans `wificredentials.py`.
 4. Appuyez sur le bouton reset de l'esp32.