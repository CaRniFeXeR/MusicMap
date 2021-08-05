import pandas as pd
from songembedding import embedd_combined_data_from_csv, embedd_combined_data
from flask import Flask, request, send_from_directory, jsonify


app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


#
# api endpoints
#
@app.route('/')
@app.route('/index')
def index():
    return send_from_directory('..\\frontend\\', "map.html")


@app.route('/scripts/<path:path>')
def send_scripts(path: str):
    return send_from_directory('..\\frontend\\scripts', path)

# todo make save


@app.route('/styles/<path:path>')
def send_styles(path: str):
    return send_from_directory('..\\frontend\\styles', path)


@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory('dist', path)


@app.route("/api/map_data/<csv_path_songs>")
def get_map_data(csv_path_songs: str):
    csv_path_playlists = "playlists.csv"
    csv_path_songs = "../" + csv_path_songs
    csv_path_playlists = "../" + csv_path_playlists
    print(f"get_map_data songs: '{csv_path_songs}'")
    data_df, (mapper, data_embedded) = embedd_combined_data(csv_path_songs, csv_path_playlists)

    print("successfully generated UMAP")

    data_combined_df = pd.concat([data_df.reset_index(), pd.DataFrame(data_embedded)], axis=1)
    data_combined_df.pop("Unnamed: 0")
    data_combined_df.pop("level_1")
    data_combined_df.rename(columns={"level_0": "type"}, inplace=True)

    print(f"concatenated data from '{csv_path_songs}' and '{csv_path_playlists}'")

    return jsonify(data_combined_df.to_json(orient="index"))


@app.route("/api/map_data_od/<csv_path_songs>")
def get_map_data_od(csv_path_songs: str):
    csv_path_playlists = "playlists.csv"
    csv_path_songs = "../" + csv_path_songs
    csv_path_playlists = "../" + csv_path_playlists
    print(f"get_map_data songs: '{csv_path_songs}'")

    data_combined_df = embedd_combined_data(csv_path_songs, csv_path_playlists, removed_columns=["danceability", "energy"])

    print(f"concatenated data from '{csv_path_songs}' and '{csv_path_playlists}'")

    return jsonify(data_combined_df.to_json(orient="index"))


@app.route("/api/embedd_music_features", methods=["POST"])
def embedd_music_features():
    content = request.json
    print("/api/embedd_music_features")
    print(content)

    data_combined_df = embedd_combined_data_from_csv(**content)

    print(f"concatenated data from '{content['csv_tracks']}' and '{content['csv_playlists']}' with removed colums '{content['removed_columns']}'")

    return jsonify(data_combined_df.to_json(orient="index"))
