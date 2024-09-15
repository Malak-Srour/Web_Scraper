am5.ready(function() {

        // Create root element
        var root = am5.Root.new("chartdiv");

        // Set themes
        root.setThemes([
            am5themes_Animated.new(root)
        ]);

        // Create chart
        var chart = root.container.children.push(
            am5xy.XYChart.new(root, {
                panX: true,
                panY: true,
                wheelX: "panX",
                wheelY: "zoomX",
                paddingLeft: 5,
                paddingRight: 5
            })
        );

        // Add cursor
        var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
        cursor.lineY.set("visible", false);

        // Create axes
        var xRenderer = am5xy.AxisRendererX.new(root, {
            minGridDistance: 60,
            minorGridEnabled: true
        });

        var xAxis = chart.xAxes.push(
            am5xy.CategoryAxis.new(root, {
                maxDeviation: 0.3,
                categoryField: "author",
                renderer: xRenderer,
                tooltip: am5.Tooltip.new(root, {})
            })
        );

        xRenderer.grid.template.setAll({
            location: 1
        });

        var yAxis = chart.yAxes.push(
            am5xy.ValueAxis.new(root, {
                maxDeviation: 0.3,
                renderer: am5xy.AxisRendererY.new(root, {
                    strokeOpacity: 0.1
                })
            })
        );

        // Create series
        var series = chart.series.push(
            am5xy.ColumnSeries.new(root, {
                name: "Articles",
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: "count",  // Number of articles
                sequencedInterpolation: true,
                categoryXField: "author"  // Author name
            })
        );

        // Update the tooltip to show the count of articles
        series.columns.template.setAll({
            width: am5.percent(80),
            fillOpacity: 0.9,
            strokeOpacity: 0,
            tooltipText: "{valueY} articles"  // Show the number of articles on hover
        });

        series.columns.template.adapters.add("fill", function(fill, target) {
            return chart.get("colors").getIndex(series.columns.indexOf(target));
        });

        series.columns.template.adapters.add("stroke", function(stroke, target) {
            return chart.get("colors").getIndex(series.columns.indexOf(target));
        });

        // Load data function
        function loadData(authorName) {
            fetch(`/articles_by_author/${authorName}`)
                .then(response => response.json())
                .then(result => {
                    let count = result.count;  // Extract the number of articles
                    let chartData = [{
                        author: authorName,
                        count: count
                    }];

                    xAxis.data.setAll(chartData);
                    series.data.setAll(chartData);
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    alert("There was an error fetching the data. Please try again.");
                });
        }

        // Event listener for the load button
        document.getElementById("loadButton").addEventListener("click", function() {
            const authorName = document.getElementById("authorInput").value;
            if (authorName) {
                loadData(authorName);
            } else {
                alert("Please enter an author name.");
            }
        });

        // Initial load with a default author
        loadData("Default Author");

    }); // end am5.ready()