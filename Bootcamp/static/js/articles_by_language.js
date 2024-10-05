am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create("chartdiv", am4charts.PieChart);

    // Add data
    fetch('/articles_by_language')
        .then(response => response.json())
        .then(data => {
            const chartData = Object.keys(data).map(key => ({
                language: key,
                count: data[key]
            }));
            chart.data = chartData;
        });

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "count";
    pieSeries.dataFields.category = "language";

}); // end am4core.ready()