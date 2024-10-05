am4core.ready(function() {

    // Fetch the data from your Flask route
    fetch('/most_negative_articles')
    .then(response => response.json())
    .then(data => {

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4plugins_timeline.SpiralChart);
        chart.levelCount = 3;
        chart.inversed = true;
        chart.endAngle = -135;
        chart.yAxisInnerRadius = 0;
        chart.yAxisRadius = am4core.percent(70);
        chart.padding(0,0,0,0)

        // Assign the fetched data to the chart
        chart.data = data;

        chart.fontSize = 11;

        var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "category";
        categoryAxis.renderer.grid.template.disabled = true;
        categoryAxis.renderer.minGridDistance = 6;
        categoryAxis.cursorTooltipEnabled = false;

        var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
        valueAxis.renderer.minGridDistance = 70;

        valueAxis.renderer.line.strokeDasharray = "1,4";
        valueAxis.renderer.line.strokeOpacity = 0.7;
        valueAxis.renderer.grid.template.disabled = true;
        valueAxis.zIndex = 100;
        valueAxis.cursorTooltipEnabled = false;
        valueAxis.min = 0;

        var series = chart.series.push(new am4plugins_timeline.CurveColumnSeries());
        series.dataFields.valueX = "value";
        series.dataFields.categoryY = "category";

        var columnTemplate = series.columns.template;
        series.tooltipText = "{categoryY}: {valueX} negative sentiment score";
        columnTemplate.adapter.add("fill", function (fill, target) {
            return chart.colors.getIndex(target.dataItem.index * 2);
        })
        columnTemplate.strokeOpacity = 0;
        columnTemplate.fillOpacity = 0.8;

        var hoverState = columnTemplate.states.create("hover");
        hoverState.properties.fillOpacity = 1;

        chart.scrollbarX = new am4core.Scrollbar();
        chart.scrollbarX.align = "center";
        chart.scrollbarX.width = am4core.percent(70);
        chart.isMeasured = false;

        var cursor = new am4plugins_timeline.CurveCursor();
        chart.cursor = cursor;
        cursor.xAxis = valueAxis;
        cursor.yAxis = categoryAxis;
        cursor.lineY.disabled = true;
        cursor.lineX.strokeDasharray = "1,4";
        cursor.lineX.strokeOpacity = 1;

        var label = chart.plotContainer.createChild(am4core.Label);
        label.text = "Most Negative Articles by Sentiment";
        label.fontSize = 15;
        label.x = am4core.percent(80);
        label.y = am4core.percent(80);
        label.horizontalCenter = "right";

    });  // End of data fetch
}); // end am4core.ready()