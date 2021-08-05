var removed_features = []

function get_embedded_data() {

}

function change_selected_features(feature_name) {

    if (removed_features.includes(feature_name)) {
        removed_features = removed_features.filter(feature => feature !== feature_name)
    } else {
        removed_features.push(feature_name)
    }

    load_data(removed_features)
}