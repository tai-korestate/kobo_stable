ifcconfig wlan0
iwconfig wlan0 essid "The Link" thelinkseoul

cd /
cd /home/pi/Kobo/kobo_dev/

git pull
python3 cap_and_send.py 
