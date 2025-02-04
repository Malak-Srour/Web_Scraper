// static/js/longest_articles_chart.js

am5.ready(function() {
  // Fetch the data from the server
  fetch('/longest_articles')
      .then(response => response.json())
      .then(data => {
          // Process the data to match the expected format
          const formattedData = data.map((item, index) => ({
              country: `${item.match(/\"(.+?)\"/)[1]} (${index + 1})`,  // Add an index to the title to make it unique
              value: parseInt(item.match(/\((\d+) words\)/)[1])  // Extract the word count
          }));

          createBarChart(formattedData);
      });

  function createBarChart(data) {
    // Create root element
    var root = am5.Root.new("chartdiv");

    // Set themes
    root.setThemes([
      am5themes_Animated.new(root)
    ]);

    // Create chart
    var chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "panX",
      wheelY: "zoomX",
      pinchZoomX: true,
      paddingLeft:0,
      paddingRight:1
    }));

    // Add cursor
    var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
    cursor.lineY.set("visible", false);

    // Create X-axis (Article Title)
    var xRenderer = am5xy.AxisRendererX.new(root, {
      minGridDistance: 30,
      minorGridEnabled: true
    });

    xRenderer.labels.template.setAll({
      rotation: -90,
      centerY: am5.p50,
      centerX: am5.p100,
      paddingRight: 15
    });

    xRenderer.grid.template.setAll({
      location: 1
    });

    var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
      maxDeviation: 0.3,
      categoryField: "country",  // This now refers to the article title
      renderer: xRenderer,
      tooltip: am5.Tooltip.new(root, {})
    }));

    var yRenderer = am5xy.AxisRendererY.new(root, {
      strokeOpacity: 0.1
    });

    var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
      maxDeviation: 0.3,
      renderer: yRenderer
    }));

    // Create series
    var series = chart.series.push(am5xy.ColumnSeries.new(root, {
      name: "Word Count",
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "value",  // Word count
      sequencedInterpolation: true,
      categoryXField: "country",  // Article title
      tooltip: am5.Tooltip.new(root, {
        labelText: "{valueY} words"
      })
    }));

    series.columns.template.setAll({ cornerRadiusTL: 5, cornerRadiusTR: 5, strokeOpacity: 0 });
    series.columns.template.adapters.add("fill", function (fill, target) {
      return chart.get("colors").getIndex(series.columns.indexOf(target));
    });

    series.columns.template.adapters.add("stroke", function (stroke, target) {
      return chart.get("colors").getIndex(series.columns.indexOf(target));
    });

    // Set data
    xAxis.data.setAll(data);
    series.data.setAll(data);

    // Make stuff animate on load
    series.appear(1000);
    chart.appear(1000, 100);
  }
});
