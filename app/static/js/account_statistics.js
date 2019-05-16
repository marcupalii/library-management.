$(function () {

    var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];
    var grey = '#C0C0C0';
    var options_pie_chart = {
        cutoutPercentage: 85,
        legend: {position: 'bottom', padding: 5, labels: {pointStyle: 'circle', usePointStyle: true}}
    };

    function get_data_book_type_statistics() {
        $.ajax({
            type: "GET",
            url: "/book_type_statistics/",
            dataType: "json",
            success: function (data) {
                create_books_type_statistics(data['types']);
            }

        });
    }

    function create_books_type_statistics(data_received) {

        let label_types = [];
        let data_types = [];
        for (key in data_received) {
            label_types.push(key);
            data_types.push(data_received[key]);
        }

        var chartData = null;
        if (data_types.length !== 0) {
            chartData = {
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
            chartData = {
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


        var chart = document.getElementById("chart-type-book");
        chart.height = 200;
        if (chart) {
            new Chart(chart, {
                type: 'pie',
                data: chartData,
                options: options_pie_chart
            });
        }
    }

    function create_statistics_2() {
        let chartData = {
            labels: ['Science', 'Literature'],
            datasets: [
                {
                    backgroundColor: colors.slice(0, 3),
                    borderWidth: 0,
                    data: [40, 45]
                }
            ]
        };
        let chart = document.getElementById("chDonut2");
        chart.height = 200;
        if (chart) {
            new Chart(chart, {
                type: 'pie',
                data: chartData,
                options: options_pie_chart
            });
        }
    }

    function create_statistics_3() {
        let chartData = {
            labels: ['Science', 'Literature', 'Other'],
            datasets: [
                {
                    backgroundColor: colors.slice(0, 3),
                    borderWidth: 0,
                    data: [21, 45, 55, 33]
                }
            ]
        };
        let chart = document.getElementById("chDonut3");
        chart.height = 200;
        if (chart) {
            new Chart(chart, {
                type: 'pie',
                data: chartData,
                options: options_pie_chart
            });
        }

    }

    get_data_book_type_statistics();
    create_statistics_2();
    create_statistics_3();


    function generateLabels() {
        if ($(window).width() < 500) {
            return ["Mar", "Apr", "May", "June", "July"]
        } else if ($(window).width() < 1024) {
            return ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"]
        } else {
            return ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
        }

    }

    function generateData() {
        if ($(window).width() < 500) {
            return [0, 5, 3, 0, 0]
        } else if ($(window).width() < 1024) {
            return [0, 5, 3, 0, 0, 0, 0]
        } else {
            return [0, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
    }

    var chartData = {
        labels: generateLabels(),
        datasets: [{
            data: generateData(),
            backgroundColor: 'transparent',
            borderColor: colors[0],
            borderWidth: 4,
            pointBackgroundColor: colors[0]
        }]
    };

    var chartTest = null;

    function create_line_chart() {

        var canvasTest = $('#chart-canvas');
        let options = {
            borderWidth: 1,
            tooltips: {
                titleFontSize: 0,
                titleMarginBottom: 0,
                bodyFontSize: 14
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontSize: 14,
                        display: true
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontSize: 14,
                        beginAtZero: true,
                        stepSize: 1
                    }
                }]
            }
        };

        chartTest = new Chart(canvasTest, {
            type: 'bar',
            data: chartData,
            maintainAspectRatio: false,
            responsive: true,
            options: options,
        });

    }

    create_line_chart();


    function resize_data(size) {
        var data = [0, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        var labels = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];


        if (size === 5) {
            if (chartTest.data.datasets[0].data.length === 12) {
                for (let i = 11; i >= 0; i--) {
                    if (i <= 1 || i >= 7) {
                        chartTest.data.datasets[0].data.splice(i, 1);
                        chartTest.data.labels.splice(i, 1);
                    }
                }

            } else if (chartTest.data.datasets[0].data.length === 7) {
                for (let i = 1; i >= 0; i--) {
                    chartTest.data.datasets[0].data.splice(i, 1);
                    chartTest.data.labels.splice(i, 1);
                }
            }
        } else if (size === 7) {
            if (chartTest.data.datasets[0].data.length === 5) {
                for (let i = 0; i < 2; i++) {
                    chartTest.data.datasets[0].data.splice(i, 0, data[i]);
                    chartTest.data.labels.splice(i, 0, labels[i]);
                }

            } else if (chartTest.data.datasets[0].data.length === 12) {
                for (let i = 11; i >= 7; i--) {
                    chartTest.data.datasets[0].data.splice(i, 1);
                    chartTest.data.labels.splice(i, 1);
                }
            }
        } else if (size === 12) {

            if (chartTest.data.datasets[0].data.length === 5) {
                for (let i = 0; i < 12; i++) {
                    if (i <= 1 || i >= 7) {
                        chartTest.data.datasets[0].data.splice(i, 0, data[i]);
                        chartTest.data.labels.splice(i, 0, labels[i]);
                    }
                }
            } else if (chartTest.data.datasets[0].data.length === 7) {
                for (let i = 7; i < 12; i++) {
                    chartTest.data.datasets[0].data.splice(i, 0, data[i]);
                    chartTest.data.labels.splice(i, 0, labels[i]);
                }
            }
        }

        chartTest.update();
    }


    var size = 0;
    $(window).resize(function () {
        if ($(window).width() < 500 && size !== 1) {
            size = 1;
            resize_data(5);
        } else if ($(window).width() > 500 && $(window).width() < 1024 && size !== 2) {
            size = 2;
            resize_data(7);
        } else if ($(window).width() >= 1024 && size !== 3) {
            size = 3;
            resize_data(12);
        }
    });

});


