import ConfigParser
import urllib
import os;
from pyItunes import *

def parseConfig(filename):	# Start the function
  parser = ConfigParser.ConfigParser();
  parser.read(filename);
  config = {};
  config['xmlFile'] = parser.get('paths', 'xmlPath');
  config['outputDir'] = parser.get('paths', 'outputDir');
  config['pattern'] = parser.get('patterns', 'old');
  config['replacement'] = parser.get('patterns', 'new');
  config['whiteList'] = [];
  for (key, value) in parser.items('playlists'):
    config['whiteList'].append(value);
  return config;

def parseXml(settings):
  data = Library(settings['xmlFile']);
  playlists = data.getPlaylistNames();
  for name in playlists:
    if (name in settings['whiteList']):
      playlist = data.getPlaylist(name);
      handle = open(settings['outputDir'].encode('utf-8') + '/'.encode('utf-8') + name.encode('utf-8'), 'w');
      handle.write('['.encode('utf-8'));
      first = True
      for song in playlist.tracks:
        if first:
          first = False
        else:
          handle.write(','.encode('utf-8'))
        path = song.location.replace(settings['pattern'], settings['replacement']).encode('utf-8');
        handle.write('\n  {\n    "service": "mpd",\n    "type": "song",\n    "title" : "'.encode('utf-8'))
        if (song.name):
          handle.write(song.name.encode('utf-8'));
        handle.write('",\n    "artist": "'.encode('utf-8'))
        if (song.artist):
          handle.write(song.artist.encode('utf-8'));
        handle.write('",\n    "album": "'.encode('utf-8'));
        if (song.album):
          handle.write(song.album.encode('utf-8'));
        handle.write('",\n    "albumart": "'.encode('utf-8'));
        albumPath = os.path.dirname(path);
        shortPath = albumPath.replace(settings['replacement'], '');
        handle.write('/albumart?web=' + urllib.quote(shortPath) + '/large&path=' + urllib.quote(albumPath) + '&icon=fa-dot-circle-o');
        handle.write('",\n    "uri": "'.encode('utf-8'));
        handle.write(path + '"\n  }'.encode('utf-8'));
        if (path == song.location):
            print 'Did not match: ' + song.location;
      handle.write('\n]\n'.encode('utf-8'));
      handle.close();

def main():
  settings = parseConfig('settings.cfg');
  parseXml(settings);

if __name__ == "__main__":
  main()
