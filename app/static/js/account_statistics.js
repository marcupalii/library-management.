$(function () {

    var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];

    function create_books_type_statistics_circle() {
        let donutOpt = {
            cutoutPercentage: 85,
            legend: {position: 'bottom', padding: 5, labels: {pointStyle: 'circle', usePointStyle: true}}
        };
        var grey = '#C0C0C0';
        let label_types = [];
        let data_types = [];
        $.each($('.statitics-type'), function () {
            label_types.push($(this).attr("id"));
            data_types.push($(this).text().trim());
        });
        var chDonutData1 = NaN;
        if (data_types.length !== 0) {
            chDonutData1 = {
                labels: label_types,
                datasets: [
                    {
                        backgroundColor: colors.slice(0, 3),
                        borderWidth: 0,
                        data: data_types
                    }
                ]
            };
        } else {
            chDonutData1 = {
                labels: ["No data to display"],
                datasets: [
                    {
                        backgroundColor: grey,
                        borderWidth: 0,
                        fillColor: grey,
                        data: [100]
                    }
                ]
            };
        }


        var chDonut1 = document.getElementById("chDonut1");
        chDonut1.height = 200;
        if (chDonut1) {
            new Chart(chDonut1, {
                type: 'pie',
                data: chDonutData1,
                options: donutOpt
            });
        }
    }


    create_books_type_statistics_circle();

    var donutOptions = {
        cutoutPercentage: 85,
        legend: {position: 'bottom', padding: 5, labels: {pointStyle: 'circle', usePointStyle: true}}
    };

// donut 2
    var chDonutData2 = {
        labels: ['Science', 'Literature'],
        datasets: [
            {
                backgroundColor: colors.slice(0, 3),
                borderWidth: 0,
                data: [40, 45]
            }
        ]
    };
    var chDonut2 = document.getElementById("chDonut2");
    chDonut2.height = 200;
    if (chDonut2) {
        new Chart(chDonut2, {
            type: 'pie',
            data: chDonutData2,
            options: donutOptions
        });
    }

// donut 3
    var chDonutData3 = {
        labels: ['Science', 'Literature', 'Other'],
        datasets: [
            {
                backgroundColor: colors.slice(0, 3),
                borderWidth: 0,
                data: [21, 45, 55, 33]
            }
        ]
    };
    var chDonut3 = document.getElementById("chDonut3");
    chDonut3.height = 200;
    if (chDonut3) {
        new Chart(chDonut3, {
            type: 'pie',
            data: chDonutData3,
            options: donutOptions
        });
    }


    var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];

    /* large line chart */
    // var chLine = document.getElementById("chLine");
    // var chartData = {
    //     labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"],
    //     datasets: [{
    //         data: [1, 5, 0, 2, 10, 3, 4],
    //         backgroundColor: 'transparent',
    //         borderColor: colors[0],
    //         borderWidth: 4,
    //         pointBackgroundColor: colors[0]
    //     }]
    // };
    //

    // if (chLine) {
    //     new Chart(chLine, {
    //         type: 'line',
    //         data: chartData,
    //         options: {
    //             scales: {
    //                 yAxes: [{
    //                     ticks: {
    //                         beginAtZero: false
    //                     }
    //                 }]
    //             },
    //             legend: {
    //                 display: false
    //             }
    //         }
    //     });
    // }

    function line_chart() {
        var chartData = {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"],
            datasets: [{
                data: [1, 5, 0, 2, 10, 3, 4],
                backgroundColor: 'transparent',
                borderColor: colors[0],
                borderWidth: 4,
                pointBackgroundColor: colors[0]
            }]
        };

        var rectangleSet = false;

        var canvasTest = $('#chart-Test');
        var chartTest = new Chart(canvasTest, {
            type: 'line',
            data: chartData,
            maintainAspectRatio: false,
            responsive: true,
            options: {
                tooltips: {
                    titleFontSize: 0,
                    titleMarginBottom: 0,
                    bodyFontSize: 12
                },
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        ticks: {
                            fontSize: 12,
                            display: false
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            fontSize: 12,
                            beginAtZero: true
                        }
                    }]
                },
                animation: {
                    onComplete: function () {
                        if (!rectangleSet) {
                            var scale = window.devicePixelRatio;

                            var sourceCanvas = chartTest.chart.canvas;
                            var copyWidth = chartTest.scales['y-axis-0'].width - 10;
                            var copyHeight = chartTest.scales['y-axis-0'].height + chartTest.scales['y-axis-0'].top + 10;

                            var targetCtx = document.getElementById("axis-Test").getContext("2d");

                            targetCtx.scale(scale, scale);
                            targetCtx.canvas.width = copyWidth * scale;
                            targetCtx.canvas.height = copyHeight * scale;

                            targetCtx.canvas.style.width = `${copyWidth}px`;
                            targetCtx.canvas.style.height = `${copyHeight}px`;
                            targetCtx.drawImage(sourceCanvas, 0, 0, copyWidth * scale, copyHeight * scale, 0, 0, copyWidth * scale, copyHeight * scale);

                            var sourceCtx = sourceCanvas.getContext('2d');

                            // Normalize coordinate system to use css pixels.

                            sourceCtx.clearRect(0, 0, copyWidth * scale, copyHeight * scale);
                            rectangleSet = true;
                        }
                    },
                    onProgress: function () {
                        if (rectangleSet === true) {
                            var copyWidth = chartTest.scales['y-axis-0'].width;
                            var copyHeight = chartTest.scales['y-axis-0'].height + chartTest.scales['y-axis-0'].top + 10;

                            var sourceCtx = chartTest.chart.canvas.getContext('2d');
                            sourceCtx.clearRect(0, 0, copyWidth, copyHeight);
                        }
                    }
                }
            }
        });
    }

    line_chart();

});

