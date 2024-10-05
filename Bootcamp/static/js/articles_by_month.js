am4core.ready(function() {

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        var chart = am4core.create("chartdiv", am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0; // this makes initial fade-in effect

        var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.dataFields.category = "month";
        categoryAxis.renderer.minGridDistance = 40;

        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

        var series = chart.series.push(new am4charts.CurvedColumnSeries());
        series.dataFields.categoryX = "month";
        series.dataFields.valueY = "count";
        series.tooltipText = "{valueY.value}";
        series.columns.template.strokeOpacity = 0;
        series.columns.template.tension = 1;

        series.columns.template.fillOpacity = 0.75;

        var hoverState = series.columns.template.states.create("hover");
        hoverState.properties.fillOpacity = 1;
        hoverState.properties.tension = 0.8;

        chart.cursor = new am4charts.XYCursor();

        // Add distinctive colors for each column using adapter
        series.columns.template.adapter.add("fill", function(fill, target) {
          return chart.colors.getIndex(target.dataItem.index);
        });

        chart.scrollbarX = new am4core.Scrollbar();
        chart.scrollbarY = new am4core.Scrollbar();

        // Function to load data for a specific year
        function loadData(year) {
            let promises = [];
            for (let month = 1; month <= 12; month++) {
                promises.push(fetch(`/articles_by_month/${year}/${month}`).then(response => response.json()));
            }

            Promise.all(promises).then(results => {
                let chartData = results.map((result, index) => {
                    const monthName = new Date(year, index).toLocaleString('default', { month: 'long' });
                    const count = parseInt(result.match(/\((\d+) articles\)/)[1]); // Extract the number of articles
                    return {
                        month: monthName,
                        count: count
                    };
                });

                chart.data = chartData;
            });
        }

        // Event listener for the load button
        document.getElementById("loadButton").addEventListener("click", function() {
            const year = document.getElementById("yearInput").value;
            loadData(year);
        });

        // Initial load with default value
        loadData(2024);

    }); // end am4core.ready()