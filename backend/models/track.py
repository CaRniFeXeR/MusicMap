from backend.models.music_features import MusicFeatures
from backend.auth import CredentialStore


class Track:

    def __init__(self, name: str = "", id: str = "", uri: str = "", **kwargs) -> None:
        self.name = name
        self.id = id
        self.uri = uri

    def calculateFeatures(self):
        sp = CredentialStore.getAuthenticatedInstance()

        features = sp.audio_features([self.id])
        if not len(features) == 1:
            raise Exception("not len(features) == 1")
        features = features[0]
        self.music_features = MusicFeatures(**features)

    @property
    def features(self) -> MusicFeatures:
        if not hasattr(self, "music_features"):
            self.calculateFeatures()

        return self.music_features
