    // Fetch the data from the server
    fetch('/articles_by_date')
        .then(response => response.json())
        .then(data => {
            // Process data into the format expected by amCharts
            const formattedData = Object.keys(data).map(date => ({
                date: new Date(date).getTime(), // Convert date to timestamp
                value: parseInt(data[date])     // Convert article count to integer
            }));
            createLineChart(formattedData);
        });

    function createLineChart(data) {
        am5.ready(function() {

            // Create root element
            var root = am5.Root.new("chartdiv");

            // Set themes
            root.setThemes([
                am5themes_Animated.new(root)
            ]);

            // Create chart
            var chart = root.container.children.push(am5xy.XYChart.new(root, {
                panX: true,
                panY: false,
                wheelX: "panX",
                wheelY: "zoomX",
                pinchZoomX: true
            }));

            // Add cursor
            var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {
                behavior: "none"
            }));
            cursor.lineY.set("visible", false);

            // Create axes
            var xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
                maxDeviation: 0.2,
                baseInterval: {
                    timeUnit: "day",
                    count: 1
                },
                renderer: am5xy.AxisRendererX.new(root, {
                    minorGridEnabled: true
                }),
                tooltip: am5.Tooltip.new(root, {}),
                extraMin: 0.1,
                extraMax: 0.1
            }));

            xAxis.get("dateFormats")["day"] = "MMM dd, yyyy";
            xAxis.get("periodChangeDateFormats")["day"] = "MMM dd, yyyy";
            xAxis.get("dateFormats")["week"] = "MMM dd, yyyy";
            xAxis.get("dateFormats")["month"] = "MMM yyyy";
            xAxis.get("periodChangeDateFormats")["month"] = "MMM yyyy";
            xAxis.get("dateFormats")["year"] = "yyyy";

            var yAxis = chart.yAxes.push(
                am5xy.ValueAxis.new(root, {
                    renderer: am5xy.AxisRendererY.new(root, {})
                })
            );

            // Add series
            var series = chart.series.push(am5xy.LineSeries.new(root, {
                name: "Articles",
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: "value",
                valueXField: "date",
                tooltip: am5.Tooltip.new(root, {
                    labelText: "{valueY} articles"
                })
            }));

            // Add scrollbar
            chart.set("scrollbarX", am5.Scrollbar.new(root, {
                orientation: "horizontal"
            }));

            // Set data
            series.data.setAll(data);

            // Make stuff animate on load
            series.appear(1000);
            chart.appear(1000, 100);

        }); // end am5.ready()
    }