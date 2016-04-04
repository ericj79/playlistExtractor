import ConfigParser
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
      handle = open(settings['outputDir'].encode('utf-8') + '/'.encode('utf-8') + name.encode('utf-8') + '.m3u'.encode('utf-8'), 'w');
      handle.write('#EXTM3U\n'.encode('utf-8'));
      for song in playlist.tracks:
        path = song.location.replace(settings['pattern'], settings['replacement']).encode('utf-8');
        handle.write('#EXTINF:'.encode('utf-8'))
        if (song.name):
          handle.write(song.name.encode('utf-8'));
        if (song.artist):
          handle.write(' - '.encode('utf-8') + song.artist.encode('utf-8'));
        handle.write('\n'.encode('utf-8'));
        handle.write(path + '\n'.encode('utf-8'));
        if (path == song.location):
            print 'Did not match: ' + song.location;
      handle.close();

def main():
  settings = parseConfig('settings.cfg');
  parseXml(settings);

if __name__ == "__main__":
  main()
