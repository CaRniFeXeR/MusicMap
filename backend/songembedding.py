from typing import Union
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn import preprocessing
import umap
import umap.plot


def embedd_csv(csv_path: str) -> Union[pd.DataFrame, Union[umap.UMAP, pd.DataFrame]]:
    song_data = pd.read_csv(csv_path, index_col=0)
    return song_data, embedd_data(song_data)


def embedd_combined_data(csv_songs: str, csv_playlists: str):

    song_data = pd.read_csv(csv_songs)
    playlist_data = pd.read_csv(csv_playlists)

    combined_df = pd.concat([song_data, playlist_data], keys=["song", "playlist"])

    return combined_df, embedd_data(combined_df)


def embedd_data(song_data: pd.DataFrame) -> Union[umap.UMAP, pd.DataFrame]:

    song_data_scaled = preprocessing.StandardScaler().fit_transform(song_data.loc[:, song_data.columns.difference(["name", "uri"])])
    mapper = umap.UMAP().fit(song_data_scaled)
    song_data_transformed = mapper.transform(song_data_scaled)

    return mapper, song_data_transformed


def visualize_embedding(mapper: umap.UMAP, hover_df: pd.DataFrame):
    p = umap.plot.interactive(mapper, hover_data=hover_df, point_size=5)
    umap.plot.show(p)


if __name__ == "__main__":
    data_df, (mapper, data_embedded) = embedd_csv("playlists.csv")

    visualize_embedding(mapper, data_df)
