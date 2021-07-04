from backend.models.music_features import MusicFeatures
from typing import List
from backend.models.track import Track
import pandas as pd


class Playlist:

    def __init__(self, name: str = "", description: str = "", **kwargs) -> None:
        self.name = name
        self.description = description
        self.tracks: List[Track] = []

    def add_track(self, track: Track):
        self.tracks.append(track)

    def calculateAverageFeatures(self):

        feature_valueList = []
        feature_names = None
        for track in self.tracks:
            if feature_names == None:
                feature_names = track.features.feature_names

            feature_valueList.append(track.features.feature_values)

        track_features_df = pd.DataFrame(feature_valueList, columns=feature_names)
        print(track_features_df.describe())

        self.avg_music_features = MusicFeatures(**dict(track_features_df.mean()))

    @property
    def avg_music_features_values(self) -> MusicFeatures:

        if not hasattr(self, "avg_music_features"):
            self.calculateAverageFeatures()

        return self.avg_music_features
