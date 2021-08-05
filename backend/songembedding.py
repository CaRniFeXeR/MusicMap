from typing import List, Union
import pandas as pd
from sklearn import preprocessing
import umap
import umap.plot


def embedd_csv(csv_path: str) -> Union[pd.DataFrame, Union[umap.UMAP, pd.DataFrame]]:
    song_data = pd.read_csv(csv_path, index_col=0)
    return song_data, embedd_data(song_data)


def embedd_combined_data_from_csv(csv_tracks: str, csv_playlists: str, removed_columns: List[str] = []) -> Union[umap.UMAP, pd.DataFrame]:
    song_data = pd.read_csv(csv_tracks)
    playlist_data = pd.read_csv(csv_playlists)

    return embedd_combined_data(song_data, playlist_data, removed_columns)


def embedd_combined_data(song_data: pd.DataFrame, playlist_data: pd.DataFrame, removed_columns: List[str] = []) -> Union[umap.UMAP, pd.DataFrame]:

    data_df = pd.concat([song_data, playlist_data], keys=["song", "playlist"]).sample(frac=1)

    mapper, data_embedded = embedd_data(data_df, removed_columns)

    data_combined_df = pd.concat([data_df.reset_index(), pd.DataFrame(data_embedded)], axis=1)
    data_combined_df.pop("Unnamed: 0")
    data_combined_df.pop("level_1")
    data_combined_df.rename(columns={"level_0": "type"}, inplace=True)
    data_combined_df = data_combined_df.reset_index()

    return data_combined_df


def embedd_data(song_data: pd.DataFrame, removed_columns: List[str] = []) -> Union[umap.UMAP, pd.DataFrame]:

    song_data_scaled = preprocessing.StandardScaler().fit_transform(song_data.loc[:, song_data.columns.difference(["name", "uri"] + removed_columns)])
    mapper = umap.UMAP().fit(song_data_scaled)
    song_data_transformed = mapper.transform(song_data_scaled)

    return mapper, song_data_transformed


def visualize_embedding(mapper: umap.UMAP, hover_df: pd.DataFrame):
    p = umap.plot.interactive(mapper, hover_data=hover_df, point_size=5)
    umap.plot.show(p)


if __name__ == "__main__":
    data_df, (mapper, data_embedded) = embedd_csv("playlists.csv")

    visualize_embedding(mapper, data_df)
