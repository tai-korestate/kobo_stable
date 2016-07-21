#Written vertically to make it easier to edit. Refactor once fully tested.


sudo apt-get --assume-yes update &&
sudo apt-get --assume-yes upgrade &&

sudo apt-get --assume-yes install git &&

sudo apt-get --assume-yes  install &&
sudo apt-get --assume-yes  install libasound-dev &&
sudo apt-get --assume-yes  install python3-pip &&
sudo apt-get --assume-yes  install portaudio19-dev python-all-dev python3-all-dev && sudo pip3 install pyaudio &&
sudo yes | pip3   install requests &&
sudo yes | pip3   install gtts &&
#vlc

sudo apt-get install vlc &&


#Jack Control 

sudo apt-get --assume-yes  install flac &&

sudo apt-get --assume-yes  install multimedia-jack &&


sudo yes | pip3 install SpeechRecognition &&



#Build Directory Bullshit

git clone https://www.github.com/tai-korestate/kobo_stable.git /home/pi/kobo_stable &&


#git clone https://www.github.com/oaubert/python-vlc.git /home/pi/kobo_stable/python-vlc

cd /home/pi/kobo_stable/python-vlc/ && sudo python3 setup.py install


cd /etc/ && sudo echo "sh /home/pi/kobo_stable/load_program.sh" > /etc/rc.local

#sudo reboot

exit 0
