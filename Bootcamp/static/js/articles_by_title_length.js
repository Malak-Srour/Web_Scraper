 am5.ready(function () {

        // Create root element
        var root = am5.Root.new("chartdiv");

        // Set themes
        root.setThemes([
            am5themes_Animated.new(root)
        ]);

        // Create chart
        var chart = root.container.children.push(am5xy.XYChart.new(root, {
            panX: false,
            panY: false,
            wheelX: "none",
            wheelY: "none",
            paddingLeft: 0
        }));

        // We don't want zoom-out button to appear while animating, so we hide it
        chart.zoomOutButton.set("forceHidden", true);

        // Create axes
        var yRenderer = am5xy.AxisRendererY.new(root, {
            minGridDistance: 20, /* Reduce minGridDistance to fit more categories */
            minorGridEnabled: true
        });

        yRenderer.grid.template.set("location", 1);
        yRenderer.labels.template.set("tooltip", null); // Disable Y-axis tooltip

        var yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
            maxDeviation: 0,
            categoryField: "category",
            renderer: yRenderer
        }));

        var xRenderer = am5xy.AxisRendererX.new(root, {
            strokeOpacity: 0.1,
            minGridDistance: 80
        });

        xRenderer.labels.template.set("tooltip", null); // Disable X-axis tooltip

        var xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root, {
            maxDeviation: 0,
            min: 0,
            numberFormatter: am5.NumberFormatter.new(root, {
                "numberFormat": "#,###a"
            }),
            extraMax: 0.1,
            renderer: xRenderer
        }));

        // Add series
        var series = chart.series.push(am5xy.ColumnSeries.new(root, {
            name: "Articles",
            xAxis: xAxis,
            yAxis: yAxis,
            valueXField: "value",
            categoryYField: "category",
            tooltip: am5.Tooltip.new(root, {
                pointerOrientation: "left",
                labelText: "{categoryY}: {valueX}" // Show category and value in colorful tooltip
            })
        }));

        // Rounded corners for columns
        series.columns.template.setAll({
            cornerRadiusTR: 5,
            cornerRadiusBR: 5,
            strokeOpacity: 0
        });

        // Make each column to be of a different color
        series.columns.template.adapters.add("fill", function (fill, target) {
            return chart.get("colors").getIndex(series.columns.indexOf(target));
        });

        series.columns.template.adapters.add("stroke", function (stroke, target) {
            return chart.get("colors").getIndex(series.columns.indexOf(target));
        });

        // Enable the cursor with only lines, no tooltip
        chart.set("cursor", am5xy.XYCursor.new(root, {
            behavior: "zoomX",
            xAxis: xAxis,
            yAxis: yAxis,
            lineY: {
                visible: true
            },
            lineX: {
                visible: true
            }
        }));

        // Fetch data from Flask API
        fetch('/articles_by_title_length')
            .then(response => response.json())
            .then(data => {
                // Set data without sorting
                yAxis.data.setAll(data);
                series.data.setAll(data);
            });

        // Make stuff animate on load
        series.appear(1000);
        chart.appear(1000, 100);

    }); // end am5.ready()