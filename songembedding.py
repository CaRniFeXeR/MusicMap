import pandas as pd
from sklearn import preprocessing
import umap
import umap.plot

playlist_df = pd.read_csv("playlists.csv", index_col=0)

playlist_scaled = preprocessing.StandardScaler().fit_transform(playlist_df.loc[:, playlist_df.columns != "name"])

mapper = umap.UMAP().fit(playlist_scaled)

p = umap.plot.interactive(mapper, hover_data=playlist_df, point_size=5)
umap.plot.show(p)
