document.getElementById("keywordForm").addEventListener("submit", function(e) {
            e.preventDefault(); // Prevent form from refreshing the page
            const keyword = document.getElementById("keyword").value;

            if (keyword) {
                // Fetch data from the Flask API with the entered keyword
                fetch(`/articles_by_keyword/${keyword}`)
                    .then(response => response.json())
                    .then(data => {
                        renderChart(data);
                    })
                    .catch(error => console.error("Error fetching data:", error));
            }
        });

        function renderChart(data) {
            am5.ready(function() {

                // Create root element
                var root = am5.Root.new("chartdiv");

                // Set themes
                root.setThemes([am5themes_Animated.new(root)]);

                // Create container for chart
                var container = root.container.children.push(am5.Container.new(root, {
                    width: am5.percent(100),
                    height: am5.percent(100),
                    layout: root.verticalLayout
                }));

                // Create series (Force Directed Tree)
                var series = container.children.push(am5hierarchy.ForceDirected.new(root, {
                    valueField: "value",
                    categoryField: "name",
                    childDataField: "children",
                    idField: "name",
                    minRadius: 50,  // Minimum size of the circles
                    maxRadius: 100,  // Maximum size of the circles
                    manyBodyStrength: -10,
                    centerStrength: 0.8
                }));

                series.data.setAll([data]); // Set the dynamic data

                series.set("selectedDataItem", series.dataItems[0]);

                // Make the chart animate
                series.appear(1000, 100);

            }); // end am5.ready()
        }