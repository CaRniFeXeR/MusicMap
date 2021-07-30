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