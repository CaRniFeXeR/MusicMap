from typing import List
from backend.models.track import Track
import pandas as pd


class Playlist:

    def __init__(self, name : str = "", description : str = "", **kwargs) -> None:
        self.name = name
        self.description = description
        self.tracks : List[Track] = []

    def add_track(self, track : Track):
        self.tracks.append(track)

    def calculateAverageFeatures(self):

        feature_valueList = []
        feature_names = None
        for track in self.tracks:
            if feature_names == None:
                feature_names = track.features.feature_names()
            
            feature_valueList.append(track.features.feature_values())
        
        trackFeatures = pd.DataFrame(feature_valueList, columns= feature_names)
        print(trackFeatures.describe())
        

    
        