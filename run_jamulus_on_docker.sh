#!/bin/bash
apt install docker docker.io curl -y 

docker pull grundic/jamulus
mkdir jam
mkdir jam/recordings
curl "https://raw.githubusercontent.com/adamane/Jamulus-deploy/main/welcome.txt" > $(pwd)/jam/welcome.txt
curl "https://raw.githubusercontent.com/adamane/Jamulus-deploy/main/toggle_rec.sh" > $(pwd)/toggle_rec.sh
sudo chmod +x toggle_rec.sh

sudo docker run \
    -e TZ=Europe/Berlin \
    --name jamulus \
    -d --rm \
    -p 22124:22124/udp \
    -v $(pwd)/jam:/jam \
    grundic/jamulus \
    -n -s -p 22124 -l /jam/jamulus.log -w /jam/welcome.txt -R /jam/recordings --norecord
