# shows acoustic features for tracks for the given artist

from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json
import spotipy
import time
import sys

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="311802bee2a04dd0b630e4e994645c15",
                                               client_secret="b869baabd55c441983b950696102d740",
                                               redirect_uri="http://floriankowarsch.com",
                                               scope="user-library-read playlist-read-private"))
# client_credentials_manager = SpotifyClientCredentials(client_id="311802bee2a04dd0b630e4e994645c15",
#                                                client_secret="b869baabd55c441983b950696102d740")
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
else:
    artist_name = 'weezer'

results = sp.search(q=artist_name, limit=2)
tids = []
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])
    tids.append(t['uri'])

start = time.time()
features = sp.audio_features(tids)
delta = time.time() - start
for feature in features:
    print(json.dumps(feature, indent=4))
    print()
    analysis = sp._get(feature['analysis_url'])
    print(json.dumps(analysis, indent=4))
    print()
print("features retrieved in %.2f seconds" % (delta,))