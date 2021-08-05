function authorize(client_id, redirect_uri, scope, response_type = "token") {
    window.location = `https://accounts.spotify.com/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope}&response_type=${response_type}`
}

function default_authorize() {
    authorize(client_id = "311802bee2a04dd0b630e4e994645c15",
        redirect_uri = "http://127.0.0.1:5000",
        scope = "user-modify-playback-state")
}

function try_get_access_token_from_url() {
    debugger;
    const queryString = window.location.search;

    const urlParams = new URLSearchParams(window.location.hash.replace("#", ""));

    const access_token = urlParams.get("access_token")

    return access_token
}

function authenticate_if_needed() {
    authenticated = false;

    access_token = try_get_access_token_from_url()

    if (access_token != null) {
        localStorage["access_token"] = access_token
        authenticated = true;
    } else {
        default_authorize()
    }

    return authenticated

}

function play_song_on_spotify(song_uri) {

    current_token = localStorage["access_token"]

    return fetch("https://api.spotify.com/v1/me/player/play", {
        method: "PUT",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
            "authorization": `Bearer ${current_token}`
        }),
        body: `{"uris": ["${song_uri}"],  "position_ms": 0}`
    }).then(response => response.json())
        .then(data => {
            console.log("successfully played song")
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function next_song_on_spotify() {

    return fetch("https://api.spotify.com/v1/me/player/next", {
        method: "POST",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
            "authorization": `Bearer ${current_token}`
        }),
        body: ``
    }).then(response => response.json())
        .then(data => {
            console.log("successfully played song")
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

function queue_song_on_spotify(song_uri) {
    current_token = localStorage["access_token"]

    return fetch(`https://api.spotify.com/v1/me/player/queue?uri=${song_uri}`, {
        method: "POST",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
            "authorization": `Bearer ${current_token}`
        }),
        body: "",
    }).then(response => {
        console.log("successfully queued")
        next_song_on_spotify().then(() => {
            console.log("successfully played next song")
        })
    })
        .catch((error) => {
            console.error('Error:', error);
        });
}

