
from typing import List
import pandas
import spotipy
from spotipy.client import Spotify
from backend.models.track import Track
from backend.models.playlist import Playlist
from backend.auth import CredentialStore


def loadUserPaylists(sp: spotipy.Spotify) -> List[Playlist]:

    parsed_paylists: List[Playlist] = []
    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']

    for playlist in playlists['items']:
        if playlist['tracks']['total'] > 0:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            results = sp.playlist(playlist['id'], fields="tracks,next")
            items = results["tracks"]["items"]

            currentPl = Playlist(**playlist)

            for item in items:
                track = Track(**item["track"])
                currentPl.add_track(track)

            currentPl.calculateAverageFeatures()
            parsed_paylists.append(currentPl)

    return parsed_paylists


if __name__ == "__main__":
    # print("hello world")

    sp = CredentialStore.getAuthenticatedInstance()
    playlists = loadUserPaylists(sp)

    avg_features_list = []
    track_feature_list = []
    for playlist in playlists:
        avg_features_list.append(playlist.avg_music_features_values.feature_values + [playlist.name])
        for track in playlist.tracks:
            track_feature_list.append(track.features.feature_values + [track.name])

    avg_features_df = pandas.DataFrame(avg_features_list, columns=playlist.avg_music_features_values.feature_names + ["name"])
    avg_features_df.to_csv("playlists.csv")

    avg_features_df = pandas.DataFrame(track_feature_list, columns=playlist.avg_music_features_values.feature_names + ["name"])
    avg_features_df.to_csv("tracks.csv")
