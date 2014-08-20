function drawSimilarityGraph(graph, elementToAppend, width, height) {

	var color = d3.scale.category20();

	var force = d3.layout.force().charge(-800).gravity(0.5).size(
			[ width, height ]).linkDistance(function(d) {
		return (1 / d.value) * 1250;
	});

	if (elementToAppend === 'graph') {
		var svg = d3.select("#graph").append("svg").attr("width", width).attr(
				"height", height)
				.attr("viewBox", "0 0 " + width + " " + height).attr(
						"preserveAspectRatio", "xMidYMid meet").style("fill",
						"rgb(125,125,125)");
	}

	else {
		var svg = elementToAppend.append("svg").attr("width", width).attr(
				"height", height)
				.attr("viewBox", "0 0 " + width + " " + height).attr(
						"preserveAspectRatio", "xMidYMid meet");
	}

	var nodeMap = {};
	graph.nodes.forEach(function(x) {
		nodeMap[x.name] = x;
	});
	graph.links = graph.links.map(function(x) {
		return {
			source : nodeMap[x.source],
			target : nodeMap[x.target],
			value : x.value
		};
	});

	// Populate the sourceLinks and targetLinks for each node.
	// Also, if the source and target are not objects, assume they are
	// indices.
	graph.nodes.forEach(function(node) {
		node.value = 0;
		node.value = 0;
	});

	graph.links.forEach(function(link) {
		link.source.value += link.value;
		link.target.value += link.value;
	});

	force.nodes(graph.nodes).links(graph.links).start();

	var link = svg.selectAll(".link").data(graph.links).enter().append("line")
			.attr("class", "link").style("stroke-width", function(d) {
				return Math.sqrt(d.value);
			});

	var node = svg.selectAll("a.node").data(graph.nodes).enter().append("a")
			.attr("class", "node").attr("xlink:href", function(d) {
				return d.name;
			}).attr("xlink:target", "_blank").append("circle").attr("class",
					"node").attr("cx", function(d) {
				return d.x;
			}).attr("cy", function(d) {
				return d.y;
			}).attr("r", function(d) {
				return Math.sqrt(d.value) / 2;
			}).style("fill", function(d) {
				return color(d.group);
			}).call(force.drag);

	var labels = svg.selectAll("text").data(graph.nodes).enter()
			.append("svg:a").attr("xlink:href", function(d) {
				return d.name;
			}).attr("xlink:target", "_blank").append("svg:text").attr({
				"x" : function(d) {
					return d.x;
				},
				"y" : function(d) {
					return d.y;
				}
			}).text(function(d) {
				return d.label;
			}).call(force.drag);

	force.on("tick", function() {

		link.attr("x1", function(d) {
			return d.source.x;
		}).attr("y1", function(d) {
			return d.source.y;
		}).attr("x2", function(d) {
			return d.target.x;
		}).attr("y2", function(d) {
			return d.target.y;
		});

		node.attr("cx", function(d) {
			return d.x;
		}).attr("cy", function(d) {
			return d.y;
		});

		labels.attr("x", function(d) {
			return d.x;
		}) // **NEW**
		.attr("y", function(d) {
			return d.y;
		});

	});
}
