import pandas as pd
from songembedding import embedd_csv
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
def send_scripts(path : str):
   return send_from_directory('..\\frontend\\scripts', path)

@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory('dist', path)


@app.route("/api/map_data/<csv_path>")
def get_map_data(csv_path: str):
    csv_path = "../" + csv_path
    print(f"get_map_data {csv_path}")
    data_df, (mapper, data_embedded) = embedd_csv(csv_path)

    data_combined_df = pd.concat([data_df, pd.DataFrame(data_embedded)], axis=1)

    print(f"concatenated data from {csv_path}")

    return jsonify(data_combined_df.to_json(orient="index"))
