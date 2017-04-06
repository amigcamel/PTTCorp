  var fill = d3.scale.category20b();
  var width = 960,
      height = 600;
      textsize = 10;
      tx = 500;
      ty = 300;
 
 
  d3.layout.cloud().size([width, height])
      .words(cands.map(function(d) {
        return {text: d, size: textsize + Math.random() * 40};
      }))
      .rotate(function(d) { return ~~(Math.random() * 5) * 30 - 60; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();

  function draw(words) {
    d3.select("#wordcloud_Hate").append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate("+tx+","+ty+")")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
  }
