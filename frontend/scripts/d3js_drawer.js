var svg, xAxis, yAxis, x, y, scaled_x, scaled_y, scatter, scatter_text, std_transitation = "";
const TRANSITION_DURATION = 4000;
const CIRCLE_STD_RADIUS = 7.5;
const CIRCLE_HIGHLIGHT_RADIUS = 12;

function handleZoom() {
    console.log("handle zoom")
    d3.select('g.chart')
        .attr('transform', d3.event.transform);
}
let zoom = d3.zoom()
    .on('zoom', handleZoom);

function initZoom() {
    d3.select('svg')
        .call(zoom);
}

function init_d3_svg() {

    // set the dimensions and margins of the graph
    margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = "95vw",
        height = "80vh";
    client_width = document.documentElement.clientWidth;
    client_height = document.documentElement.clientHeight;

    // append the svg object to the body of the page
    svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        // .call(d3.zoom().on("zoom", function () {
        //     svg.attr("transform", d3.event.transform)
        //  }))
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Set the zoom and Pan features: how much you can zoom, on which part, and what to do when there is a zoom
    zoom = d3.zoom()
        .scaleExtent([.1, 20])  // This control how much you can unzoom (x0.5) and zoom (x20)
        // .extent([[0, 0], [width, height]])
        .on("zoom", updatePositionOnZoom);

    // This add an invisible rect on top of the chart area. This rect can recover pointer events: necessary to understand when the user zoom
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(zoom);
    // now the user can zoom and it will trigger the function called updatePositionOnZoom

    // Add X axis
    x = d3.scaleLinear()
        .domain([4, 8])
        .range([0, client_width]);
    scaled_x = x;
    xAxis = svg.append("g")
        .attr("transform", "translate(0," + client_height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    y = d3.scaleLinear()
        .domain([0, 9])
        .range([client_height, 0]);
    scaled_y = y;
    yAxis = svg.append("g")
        .call(d3.axisLeft(y));

    scatter = svg.append('g')

    std_transitationFactory = () => svg.transition().duration(TRANSITION_DURATION).ease(d3.easeQuadInOut);

}

// A function that updates the chart when the user zoom and thus new boundaries are available
function updatePositionOnZoom() {

    current_zoom_level = d3.event.transform.k
    console.log("zoom factor " + current_zoom_level)

    let display_text = current_zoom_level <= 2.5 ? "none" : "block"

    // recover the new scale
    scaled_x = d3.event.transform.rescaleX(x);
    scaled_y = d3.event.transform.rescaleY(y);

    // update axes with these new boundaries
    xAxis.call(d3.axisBottom(scaled_x))
    yAxis.call(d3.axisLeft(scaled_y))

    // update circle position
    scatter
        .selectAll("circle")
        .attr('cx', function (d) { return scaled_x(d["0"]) })
        .attr('cy', function (d) { return scaled_y(d["1"]) });

    scatter
        .selectAll("text")
        .attr('x', function (d) { return scaled_x(d["0"]) })
        .attr('y', function (d) { return scaled_y(d["1"]) })

    scatter
        .selectAll("text.song_text")
        .style("display", display_text);


}


function plot_songs(data) {

}

function plot_playlists() {

}

function plot_data(data) {

    scatter_circles = scatter
        .selectAll("circle")
        .data(data, function (d) { return d.uri })

    scatter_text = scatter
        .selectAll("text")
        .data(data, function (d) { return d.uri })

    draw_data()
}

function replot_data(data) {
    plot_data(data)
}

function draw_data() {

    scatter_circles
        .join(
            enter => enter.append("circle")
                .attr("cx", function (d) { return scaled_x(d["0"]); })
                .attr("cy", function (d) { return scaled_y(d["1"]); })
                .attr("r", CIRCLE_STD_RADIUS),
            update => update
                .call(update => update.transition(std_transitationFactory())
                    .attr("cx", function (d) { return scaled_x(d["0"]); })
                    .attr("cy", function (d) { return scaled_y(d["1"]); })

                )
        )
        .style("pointer-events", "visible")
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut)
        .classed("song", function (d) { return d.type == "song" })
        .classed("playlist", function (d) { return d.type == "playlist" })
        .on("click", function (d) {
            // alert("clicked!")
            if (d.type == "song") {
                console.log("clicked: " + d.name + " " + d.uri)
                play_song_on_spotify(d.uri)
            }
        });

    scatter_text
        .join(
            enter => enter.append("text")
                .text(function (d) {
                    return d.name;
                })
                .attr("x", function (d) {
                    return x(d["0"]);
                })
                .attr("y", function (d) {
                    return y(d["1"]);
                }),
            update => update
                .call(update => update.transition(std_transitationFactory())
                    .attr("y", function (d) { return y(d["1"]); })
                    .attr("x", function (d) { return x(d["0"]); })
                )
        )
        .style("font-size", "14px")
        .classed("song_text", function (d) { return d.type == "song" })
        .classed("playlist_text", function (d) { return d.type == "playlist" })
}

//transitions

function handleMouseOver(d, i) {
    d3.select(this).transition()
        .duration(1)
        .attr("r", CIRCLE_HIGHLIGHT_RADIUS);
}

function handleMouseOut(d, i) {
    d3.select(this).transition()
        .duration(1)
        .attr("r", CIRCLE_STD_RADIUS);
}