#!/bin/bash

#### prep system
echo "deb https://packages.cloud.google.com/apt aiyprojects-stable main" | sudo tee /etc/apt/sources.list.d/aiyprojects.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get upgrade

#### install voice hat
## enable voice hat -- included already in provided /boot/config.txt
# echo "dtoverlay=googlevoicehat-soundcard" | sudo tee -a /boot/config.txt
## disable built-in audio -- included already in provided /boot/config.txt
# sudo sed -i -e "s/^dtparam=audio=on/#\0/" /boot/config.txt

#### install pulseaudio
sudo apt-get install -y pulseaudio
sudo mkdir -p /etc/pulse/daemon.conf.d/
echo "default-sample-rate = 48000" | sudo tee /etc/pulse/daemon.conf.d/aiy.conf
sudo sed -i -e "s/^load-module module-suspend-on-idle/#load-module module-suspend-on-idle/" /etc/pulse/default.pa

#### install required packages
sudo apt-get install -y git python3-pip mpg123
## install aiy projects python library, not needed in current implementation
# sudo pip3 install -e AIY-projects-python

#### set up included files and services
sudo mv staging/boot/config.txt /boot/config.txt
mv staging/home/aj/jukebox.py /home/aj/jukebox.py
chmod +x /home/aj/jukebox.py
mv staging/home/aj/.config/systemd/user/jukebox.service /home/aj/.config/systemd/user/jukebox.service
systemctl --user daemon-reload
systemctl --user enable jukebox.service

#### reboot
sudo reboot