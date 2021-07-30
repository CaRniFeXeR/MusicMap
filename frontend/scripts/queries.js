function runMapQuery(path) {
    fetch(`${window.origin}/` + path, {
        method: "GET",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}