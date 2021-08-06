
from typing import Dict, List
import pandas
import spotipy
from spotipy.client import Spotify
from backend.models.track import Track
from backend.models.playlist import Playlist
from backend.auth import CredentialStore


def _get_user_playlists(sp: spotipy.Spotify, offset: int = 0) -> List[Dict]:
    playlists_loaded = sp.current_user_playlists(offset=offset)
    return playlists_loaded["items"]


def _get_all_users_playlists(sp: spotipy.Spotify) -> List[Dict]:

    current_request_contained_paylists = True
    offset = 0
    playlists = []
    while current_request_contained_paylists:
        current_playlist_batch = _get_user_playlists(sp, offset)
        playlists += current_playlist_batch
        offset += len(current_playlist_batch)
        current_request_contained_paylists = len(current_playlist_batch) > 0

    return playlists


def loadUserPaylists(sp: spotipy.Spotify) -> List[Playlist]:

    parsed_paylists: List[Playlist] = []

    playlists = _get_all_users_playlists(sp)

    for playlist in playlists:
        if playlist['tracks']['total'] > 0:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            results = sp.playlist(playlist['id'], fields="tracks,next")
            items = results["tracks"]["items"]

            currentPl = Playlist(**playlist)

            for item in items:
                if not item is None:
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
    track_names_set = {"a"}
    for playlist in playlists:
        avg_features_list.append(playlist.avg_music_features_values.feature_values + [playlist.name, playlist.uri])
        for track in playlist.tracks:
            if not track.name in track_names_set:
                track_feature_list.append(track.features.feature_values + [track.name, track.uri])
                track_names_set.add(track.name)
            else:
                print(f"canceled '{track.name}' due to duplication")

    # todo add playlist uri
    avg_features_df = pandas.DataFrame(avg_features_list, columns=playlist.avg_music_features_values.feature_names + ["name", "uri"])
    avg_features_df.to_csv("playlists.csv")

    avg_features_df = pandas.DataFrame(track_feature_list, columns=playlist.avg_music_features_values.feature_names + ["name", "uri"])
    avg_features_df.to_csv("tracks.csv")
