
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


function plot_data(data) {


    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = "95vw",
        height = "80vh";
    client_width = document.documentElement.clientWidth;
    client_height = document.documentElement.clientHeight;

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
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
        .on("zoom", updateChart);

    // This add an invisible rect on top of the chart area. This rect can recover pointer events: necessary to understand when the user zoom
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(zoom);
    // now the user can zoom and it will trigger the function called updateChart

    //add zoom and panning
    // initZoom()

    // Add X axis
    var x = d3.scaleLinear()
        .domain([4, 8])
        .range([0, client_width]);
    var xAxis = svg.append("g")
        .attr("transform", "translate(0," + client_height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 9])
        .range([client_height, 0]);
    var yAxis = svg.append("g")
        .call(d3.axisLeft(y));

    // Add dots
    var scatter = svg.append('g')
    // .attr("clip-path", "url(#clip)")

    scatter_data = scatter
        .selectAll("circle")
        .data(data)
        .enter()

    scatter_data
        .append("circle")
        .attr("cx", function (d) { return x(d["0"]); })
        .attr("cy", function (d) { return y(d["1"]); })
        .attr("r", 7.5)
        .style("fill", "#69b3a2")
        .style("pointer-events", "visible")
        .on("click", function (d) {
            // alert("clicked!")
            console.log("clicked: " + d.name + " " + d.uri)
            play_song_on_spotify(d.uri)
        })
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);

    scatter_data
        .append("text")
        .text(function (d) {
            return d.name;
        })
        .attr("x", function (d) {
            return x(d["0"]);
        })
        .attr("y", function (d) {
            return y(d["1"]);
        })
        .style("font-size", "14px");



    // A function that updates the chart when the user zoom and thus new boundaries are available
    function updateChart() {

        current_zoom_level = d3.event.transform.k
        console.log("zoom factor " + current_zoom_level)

        let display_text = current_zoom_level <= 1.5 ? "none" : "block"

        // recover the new scale
        var newX = d3.event.transform.rescaleX(x);
        var newY = d3.event.transform.rescaleY(y);

        // update axes with these new boundaries
        xAxis.call(d3.axisBottom(newX))
        yAxis.call(d3.axisLeft(newY))

        // update circle position
        scatter
            .selectAll("circle")
            .attr('cx', function (d) { return newX(d["0"]) })
            .attr('cy', function (d) { return newY(d["1"]) });

        scatter
            .selectAll("text")
            .attr('x', function (d) { return newX(d["0"]) })
            .attr('y', function (d) { return newY(d["1"]) })
            .style("display", display_text);


    }

    //transitions

    function handleMouseOver(d, i) {
        d3.select(this).transition()
            .duration(1)
            .attr("r", 12);
    }

    function handleMouseOut(d, i) {
        d3.select(this).transition()
            .duration(1)
            .attr("r", 7.5);
    }
}