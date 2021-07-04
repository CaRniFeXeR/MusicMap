from typing import List


class MusicFeatures:

    def __init__(self, danceability : float, energy : float, loudness : float, speechiness: float,  acousticness: float, instrumentalness : float, liveness : float, valence: float, tempo: float) -> None:
        self.danceability = danceability
        self.energy = energy
        self.loudness = loudness
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo

    @property
    def feature_names(self) -> List[str]:
        names = self.keys()
        return names
    
    @property
    def feature_values(self) -> List[float]:
        variables = self.feature_names()
        feature_values = [getattr(self, v) for v in variables]

        return feature_values

