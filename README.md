# playlistExtractor

Python script used to generate Volumio 2 playlists from iTunes library.

The purpose is that if you have your iTunes library backed up to a network drive, or just stored on a network drive, you can point this script at it and update your playlists in volumio from it.
This requires pyitunes (https://github.com/liamks/pyitunes). It can run on a crontab job to update things regularly.
You can install pyItunes using pip. If pip is not installed:
sudo apt-get update
sudo apt-get install python-pip

Then to install the module:
sudo pip install git+https://github.com/liamks/libpytunes.git

An example crontab entry is:
\*/2 9-21 \* \* \* cd /home/volumio/playlistExtractor && nice -10 python playlistExtractor.py
