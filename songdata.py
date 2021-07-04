
from backend.models.track import Track
from backend.models.playlist import Playlist
from backend.auth import CredentialStore


if __name__ == "__main__":
    # print("hello world")

    sp = CredentialStore.getAuthenticatedInstance()
    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            
            currentPl = Playlist(**playlist)

            for track in tracks:
                track_model = Track(**track)
                currentPl.add_track(track_model)

            currentPl.calculateAverageFeatures()