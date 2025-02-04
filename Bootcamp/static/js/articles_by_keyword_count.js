am5.ready(function() {

  // Create root element
  var root = am5.Root.new("chartdiv");

  // Set themes
  root.setThemes([
    am5themes_Animated.new(root)
  ]);

  // Create chart
  var chart = root.container.children.push(am5radar.RadarChart.new(root, {
    panX: false,
    panY: false,
    wheelX: "none",
    wheelY: "none",
    startAngle: -84,
    endAngle: 264,
    innerRadius: am5.percent(40)
  }));

  // Add cursor
  const cursor = chart.set("cursor", am5radar.RadarCursor.new(root, {
    behavior: "zoomX"
  }));
  cursor.lineY.set("forceHidden", true);

  // Add scrollbar
  chart.set("scrollbarX", am5.Scrollbar.new(root, {
    orientation: "horizontal",
    exportable: false
  }));

  // Create axes
  var xRenderer = am5radar.AxisRendererCircular.new(root, {
    minGridDistance: 30
  });
  xRenderer.grid.template.set("forceHidden", true);

  var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
    maxDeviation: 0,
    categoryField: "category",
    renderer: xRenderer
  }));

  var yRenderer = am5radar.AxisRendererRadial.new(root, {});
  yRenderer.labels.template.set("centerX", am5.p50);

  var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
    maxDeviation: 0.3,
    min: 0,
    renderer: yRenderer
  }));

  // Add series
  var series = chart.series.push(am5radar.RadarColumnSeries.new(root, {
    name: "Series 1",
    sequencedInterpolation: true,
    xAxis: xAxis,
    yAxis: yAxis,
    valueYField: "value",
    categoryXField: "category"
  }));

  // Rounded corners for columns
  series.columns.template.setAll({
    cornerRadius: 5,
    tooltipText: "{categoryX}: {valueY}"
  });

  // Make each column to be of a different color
  series.columns.template.adapters.add("fill", function (fill, target) {
    return chart.get("colors").getIndex(series.columns.indexOf(target));
  });

  series.columns.template.adapters.add("stroke", function (stroke, target) {
    return chart.get("colors").getIndex(series.columns.indexOf(target));
  });

  // Fetch data from the server
  fetch('/articles_by_keyword_count')
    .then(response => response.json())
    .then(data => {
        // Format the data to fit the chart structure
        const formattedData = Object.keys(data).map(key => ({
            category: key,  // Just the number of keywords, no additional text
            value: data[key]  // Count of articles
        }));

        xAxis.data.setAll(formattedData);
        series.data.setAll(formattedData);
    });

  // Make stuff animate on load
  series.appear(1000);
  chart.appear(1000, 100);

}); // end am5.ready()