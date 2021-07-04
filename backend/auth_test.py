import spotipy
from spotipy.oauth2 import SpotifyOAuth



def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))


if __name__ == '__main__':

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="311802bee2a04dd0b630e4e994645c15",
                                               client_secret="b869baabd55c441983b950696102d740",
                                               redirect_uri="http://floriankowarsch.com",
                                               scope="user-library-read playlist-read-private"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)

            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)