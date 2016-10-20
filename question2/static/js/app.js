$(function () {
    scope_data = null;
    var product1filtered = [];
    var product2filtered = [];
    var renderGraph = function() {
        var data = JSON.parse(JSON.stringify(scope_data));
        $("svg").html('');
        nodes = []
        for(var i = 0; i < data.nodes.length; i++){
            if(data.nodes[i].id.startsWith('product1') && (product1filtered.length == 0 || product1filtered.includes(data.nodes[i].id))) {
                nodes.push(data.nodes[i]);
            }
            if(data.nodes[i].id.startsWith('product2') && (product2filtered.length == 0 || product2filtered.includes(data.nodes[i].id))) {
                nodes.push(data.nodes[i]);
            }
        }
        data.nodes = nodes.sort(compare_node_group);
        console.log(JSON.stringify(nodes))
        links = []
        for(var i = 0; i < data.links.length; i++){
            if ((product1filtered.length == 0 || product1filtered.includes(data.links[i].source)) && 
                (product2filtered.length == 0 || product2filtered.includes(data.links[i].target))){
                links.push(data.links[i]);
            }
        }
        data.links = links;

        // Get color scheme from d3
        var color = d3.scaleOrdinal(d3.schemeCategory20);

        // d3 graph rendering
        var svg = d3.select("svg"),
            width = +svg.attr("width"),
            height = +svg.attr("height");

        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function (d) {
                return d.id;
            }))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2));


        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
            .attr("stroke-width", function (d) {
                return Math.sqrt(d.value);
            });

        var node = svg.selectAll("g.gnode")
            .attr("class", "gnode")
            .data(data.nodes)
            .enter().append("g")

        var circle = node.append("circle")
            .attr("class", "node")
            .attr("r", 15)
            .attr("fill", function (d) {
                return color(d.group);
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        var label = node.append("text")
            .text(function (d) {
                return d.id.split(".")[1];
            }).attr("x", -9).attr("y", 4);

        simulation
            .nodes(data.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(data.links);

        function ticked() {
            link
                .attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            node
                .attr("cx", function (d) {
                    return d.x;
                })
                .attr("cy", function (d) {
                    return d.y;
                })
                .attr("transform", function (d) {
                    return 'translate(' + [d.x, d.y] + ')';
                });
        }

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        return color;
    };

    function compare_node_group(a,b) {
        if (a['group'] < b['group'])
            return -1;
        if (a['group'] > b['group'])
            return 1;
        return 0;
    }

    var renderDataTable = function(color_function) {
        var data = jQuery.extend(true, {}, scope_data);
        // Mustache rendering
        var template = $('#template').html();
        data.color1 = color_function(1);
        data.color2 = color_function(2);
        var rendered = Mustache.render(template, data);
        $('#data').html(rendered);
    }

    var renderFilterTemplate = function(color_function) {
        var data = jQuery.extend(true, {}, scope_data);
        data.product1filters = [];
        data.product2filters = [];
        for(var i = 0; i < data.rows.length; i++) {
            if (data.product1filters.includes(data.rows[i].product1) == false) {
                data.product1filters.push(data.rows[i].product1);
            }
            if (data.product2filters.includes(data.rows[i].product2) == false) {
                data.product2filters.push(data.rows[i].product2);
            }
        }
        data.product1filters = data.product1filters.sort();
        data.product2filters = data.product2filters.sort();
        // Mustache rendering
        var template = $('#filter-template').html();
        data.color1 = color_function(1);
        data.color2 = color_function(2);
        var rendered = Mustache.render(template, data);
        $('#filters').html(rendered);
    }

    var applyFilters = function() {
        product1filtered = [];
        product2filtered = [];
        $('#filters input[type=checkbox]').each(function(){
            if ($(this).is(':checked')) {
                if ($(this).data('id').startsWith('product1')) {
                    product1filtered.push($(this).data('id'))
                }
                else {
                    product2filtered.push($(this).data('id'))
                }
            }
        });
    };

    var initializeData = function() {
        $.get('/api/data', function (data) {
            scope_data = data;
            
            var color_function = renderGraph();
            renderDataTable(color_function)
            renderFilterTemplate(color_function)
        });
    }

    $(document).on('click', 'input[type=checkbox]', function(sender){
        applyFilters();
        renderGraph();
    });

    initializeData();
});
