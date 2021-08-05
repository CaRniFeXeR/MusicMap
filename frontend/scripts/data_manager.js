var removed_features = []
var data_dict = {}

async function get_embedded_data() {
    selection_key = removed_features.join("-")

    if (selection_key in data_dict) {
        return data_dict[selection_key]
    } else {
        data = await embedd_data("../tracks.csv", "../playlists.csv", removed_features);
        data_dict[selection_key] = data
        return data
    }

}

function change_selected_features(feature_name) {

    if (removed_features.includes(feature_name)) {
        removed_features = removed_features.filter(feature => feature !== feature_name)
    } else {
        removed_features.push(feature_name)
    }
    removed_features = removed_features.sort()

    load_data()
}


function load_data() {
    get_embedded_data().then((data) => {
        console.log(data)
        plot_data(data)
    })
}