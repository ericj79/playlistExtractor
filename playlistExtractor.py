"""Create Volumio 2 playlist files from an iTunes library XML file"""

import ConfigParser
import urllib
import os
from libpytunes import Library


def parse_config(filename):
    """Parse the config settings into an object."""
    # Start the function
    parser = ConfigParser.ConfigParser()
    parser.read(filename)
    config = {}
    config['xmlFile'] = parser.get('paths', 'xmlPath')
    timestamp = 0
    if parser.has_option('paths', 'xmlPathTimestamp'):
        timestamp = parser.getfloat('paths', 'xmlPathTimestamp')

    filetime = os.path.getmtime(config['xmlFile'])
    if filetime > timestamp:
        parser.set('paths', 'xmlPathTimestamp', filetime)
        filehandle = open(filename, 'w')
        parser.write(filehandle)
        filehandle.close()
    else:
        exit()

    config['outputDir'] = parser.get('paths', 'outputDir')
    config['pattern'] = parser.get('patterns', 'old')
    config['replacement'] = parser.get('patterns', 'new')
    config['whiteList'] = []
    playlists = dict(parser.items('playlists'))
    for value in playlists.values():
        config['whiteList'].append(value)
    return config


def converttobytestr(orig):
    """Make sure this thing is a byte string"""
    if isinstance(orig, unicode):
        return orig.encode('ascii', 'xmlcharrefreplace').replace('"', '\\"')
    elif isinstance(orig, str):
        return orig.replace('"', '\\"')
    else:
        return ''


def parse_xml(settings):
    """Parse the XML file for the wanted playlists and write the data to a file."""
    data = Library(settings['xmlFile'])
    playlists = data.getPlaylistNames()
    for name in playlists:
        if name in settings['whiteList']:
            playlist = data.getPlaylist(name)
            handle = open(settings['outputDir'] +
                          '/' + name, 'w')
            handle.write('[')
            first = True
            for song in playlist.tracks:
                if first:
                    first = False
                else:
                    handle.write(',')
                path = converttobytestr(song.location).replace(
                    settings['pattern'], settings['replacement'])
                handle.write(
                    '\n  {\n    "service": "mpd",\n    "type": "song",\n    "title" : "')
                if song.name:
                    handle.write(converttobytestr(song.name))
                handle.write('",\n    "artist": "')
                if song.artist:
                    handle.write(converttobytestr(song.artist))
                handle.write('",\n    "album": "')
                if song.album:
                    handle.write(converttobytestr(song.album))
                handle.write('",\n    "albumart": "')
                album_path = os.path.dirname(path)
                short_path = album_path.replace(settings['replacement'], '')
                # handle.write('/albumart?web=none')
                handle.write('/albumart?web=' + urllib.quote(short_path) +
                             '/large&path=' + urllib.quote(album_path) + '&icon=fa-dot-circle-o')
                handle.write('",\n    "uri": "')
                handle.write(path + '"\n  }')
                if path == song.location:
                    print 'Did not match: ' + song.location
            handle.write('\n]\n')
            handle.close()


def main():
    """Main function"""
    settings = parse_config('settings.cfg')

    # check the modified time of the file to see if we have an update
    statbuf = os.stat(settings['xmlFile'])
    parse_xml(settings)


if __name__ == "__main__":
    main()
