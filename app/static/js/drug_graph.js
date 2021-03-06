function drawGraphForDrug(service_url, uri, id) {

	$("#graph").empty();
	$("#loading").show();

	$.get(service_url, {
		'type' : 'drugs',
		'uri' : uri,
		'id' : id
	}, function(data) {
		$("#loading").hide();
		if (data.graph.links.length > 0) {
			drawDrugGraph(service_url, data.graph);
		} else {
			$("#noresponse").show();
		}
	});
}

function drawDrugGraph(service_url, graph) {
	var width = 600, height = 600;

	var color = d3.scale.category10();

	var force = d3.layout.force().charge(-200).gravity(.1).linkDistance(160)
			.size([ width, height ]);

	var svg = d3.select("#graph").append("svg").attr("width", width).attr(
			"height", height);

	force.nodes(graph.nodes).links(graph.links).start();

	var link = svg.selectAll(".link").data(graph.links).enter().append("line")
			.attr("class", "link").style("stroke-width", function(d) {
				return Math.sqrt(d.value);
			});

	var node = svg.selectAll("circle.node").data(graph.nodes).enter().append(
			"circle").attr("class", "node").attr("r", function(d) {
		return (d.degree * 2 + 5);
	}).style("fill", function(d) {
		return color(d.type);
	}).on("click", function(d) {
		click(d);
	}).call(force.drag);

	node.append("title").text(function(d) {
		return d.label;
	});

	var texts = svg.selectAll("text.label").data(graph.nodes).enter().append(
			"text").attr("class", "label").attr("fill", "black").style(
			"text-anchor", "middle").attr("class", function(d) {
		return d.type;
	}).text(function(d) {
		if (d.type != 'criterion') {
			return d.label;
		} else {
			return '';
		}
	});

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

		texts.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")";
		});
	});

	function click(n) {
		if (n.type == 'drug') {
			drawGraphForDrug(service_url, n.uri, n.label);
		}
	}
}
