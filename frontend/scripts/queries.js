function runMapQuery(path) {
    return fetch(`${window.origin}/` + path, {
        method: "GET",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response => response.json())
        .then(data => {
            console.log("recived data")
            data_parsed = Object.values(JSON.parse(data))
            return data_parsed
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

async function executePostRequest(path, data) {
    const response = await fetch(`${window.origin}/` + path, {
        method: "POST",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        }),
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function embedd_data(csv_tracks, csv_playlists, removed_columns) {

    var request = {
        "csv_tracks": csv_tracks,
        "csv_playlists": csv_playlists,
        "removed_columns": removed_columns
    }

    try {
        const data = await executePostRequest("/api/embedd_music_features", request);
        console.log("recived data");
        data_parsed = Object.values(JSON.parse(data));
        return data_parsed;
    } catch (error) {
        console.error('Error:', error);
    }
}