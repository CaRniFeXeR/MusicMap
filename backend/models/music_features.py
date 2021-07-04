from typing import List


class MusicFeatures:

    def __init__(self, danceability: float = None, energy: float = None, loudness: float = None, speechiness: float = None,  acousticness: float = None, instrumentalness: float = None, liveness: float = None, valence: float = None, tempo: float = None, **kwargs) -> None:
        self.danceability = danceability
        self.energy = energy
        self.loudness = loudness
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo  # excluded temp

    @property
    def feature_names(self) -> List[str]:
        names = list(vars(self).keys())
        return names

    @property
    def feature_values(self) -> List[float]:
        variables = self.feature_names
        feature_values = [getattr(self, v) for v in variables]

        return feature_values
