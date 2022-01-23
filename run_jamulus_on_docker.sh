#!/bin/bash
sudo apt-get update
sudo apt-get install \
   apt-transport-https \
   ca-certificates \
   curl \
   gnupg \
   lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg


echo \
 "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io -y
sudo apt upgrade -y


docker pull ghcr.io/adamane/jamulus_contakt:3_7_0 # Still download this for legacy
docker pull ghcr.io/adamane/jamulus_contakt:3_8_1
mkdir jam
mkdir jam/recordings
curl "https://raw.githubusercontent.com/adamane/Jamulus-deploy/main/serverfiles/welcome.txt" > $(pwd)/jam/welcome.txt
curl "https://raw.githubusercontent.com/adamane/Jamulus-deploy/main/serverfiles/toggle_rec.sh" > $(pwd)/toggle_rec.sh
curl "https://raw.githubusercontent.com/adamane/Jamulus-deploy/main/serverfiles/install_appliences.sh" > $(pwd)/install_appliences.sh
echo "
#!/bin/bash
sudo docker run \
    -e TZ=Europe/Berlin \
    --name jamulus \
    -d --rm \
    -p 22124:22124/udp \
    -v $(pwd)/jam:/jam \
    ghcr.io/adamane/jamulus_contakt:3_7_0 -n -s -p 22124 -l /jam/jamulus.log -w /jam/welcome.txt -R /jam/recordings --norecord -u 50" > run_server_legacy.sh

echo "
#!/bin/bash
sudo docker run \
    -e TZ=Europe/Berlin \
    --name jamulus \
    -d --rm \
    -p 22124:22124/udp \
    -v $(pwd)/jam:/jam \
    ghcr.io/adamane/jamulus_contakt:3_8_1 -n -s -p 22124 -l /jam/jamulus.log -w /jam/welcome.txt -R /jam/recordings --norecord -u 50" > run_server.sh
sudo chmod +x $(pwd)/toggle_rec.sh
sudo chmod +x $(pwd)/run_server.sh
sudo chmod +x $(pwd)/install_appliences.sh

./run_server.sh


