$(function () {
    let c1 = '#007bff';
    let c2 = '#28a745';
    let c3 = '#333333';
    let c4 = '#c3e6cb';
    let c5 = '#dc3545';
    let c6 = '#6c757d';

    var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];
    var grey = '#E5E5E5';
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
        // let data_received = get_data_book_type_statistics();
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

    function get_data_user_trust_coeff() {
        $.ajax({
            type: "GET",
            url: "/user_trust_coeff_statistics/",
            dataType: "json",
            success: function (data) {
                create_user_trust_coeff_statistics(data['coeff']);
            }
        });
    }

    function create_user_trust_coeff_statistics(coeff) {
        let labels = [];
        let data = [Math.abs(coeff), 100 - Math.abs(coeff)];
        let backgroundColor = grey;
        if (coeff < 0) {
            labels.push("late");
            backgroundColor = "#dc3545";
        } else if (coeff > 0) {
            labels.push("earlier");
            backgroundColor = colors[1];
        } else {
            labels.push("no data")
        }

        let options = {
            legend: {position: 'bottom', padding: 5, labels: {pointStyle: 'circle', usePointStyle: true}},
            responsive: true,
            maintainAspectRatio: false,
            cutoutPercentage: 85,
            tooltips: {enabled: false},
            hover: {mode: null}
        };
        let chartData = {
            labels: labels,
            datasets: [{
                backgroundColor: [backgroundColor],
                data: data
            }]
        };

        let plugin_setting = [{
            beforeDraw: function (chart) {
                let width = chart.chart.width,
                    height = chart.chart.height,
                    ctx = chart.chart.ctx;

                ctx.restore();
                let fontSize = (height / 150).toFixed(2);
                ctx.font = fontSize + "em sans-serif";
                ctx.fillStyle = "#9b9b9b";
                ctx.textBaseline = "middle";

                let text = Math.abs(coeff).toString() + '%',
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = height / 2.4;

                ctx.fillText(text, textX, textY);
                ctx.save();
            }
        }];

        var chart = document.getElementById("chart-user-trust-coeff");
        chart.height = 200;
        if (chart) {
            new Chart(chart, {
                type: 'pie',
                data: chartData,
                plugins: plugin_setting,
                options: options
            });
        }
    }

    function get_data_books_count() {
        $.ajax({
            type: "GET",
            url: "/books_count/",
            dataType: "json",
            success: function (data) {
                create_books_statistics(data);
            }
        });
    }

    function create_books_statistics(books) {
        let chartData = NaN;
        if (books['total'] !== 0) {
            chartData = {
                labels: ['Total', 'Failed'],
                datasets: [
                    {
                        backgroundColor: colors.slice(0, 3),
                        borderWidth: 0,
                        data: [books['total'], books['failed']]
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
    get_data_user_trust_coeff();
    get_data_books_count();


    function generateLabels() {
        if ($(window).width() < 500) {
            return ["Mar", "Apr", "May", "June", "July"]
        } else if ($(window).width() < 1024) {
            return ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"]
        } else {
            return ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
        }

    }

    var data_per_month_late = [];
    var data_per_month_in_time = [];

    function generateData(type) {
        let response = [];
        if ($(window).width() < 500) {
            if (type === "late") {
                for (let i = 0; i < 5; i++) {
                    response.push(data_per_month_late[i])
                }
            } else {
                for (let i = 0; i < 5; i++) {
                    response.push(data_per_month_in_time[i])
                }
            }
            return response
        } else if ($(window).width() < 1024) {
            if (type === "late") {
                for (let i = 0; i < 7; i++) {
                    response.push(data_per_month_late[i])
                }
            } else {
                for (let i = 0; i < 7; i++) {
                    response.push(data_per_month_in_time[i])
                }
            }
            return response
        } else {
            if (type === "late") {
                return data_per_month_late
            } else {
                return data_per_month_in_time
            }
        }
    }


    var chartTest = null;

    function create_line_chart(chartData) {

        var canvasTest = $('#chart-canvas');
        let options = {
            borderWidth: 1,
            tooltips: {
                titleFontSize: 0,
                titleMarginBottom: 0,
                bodyFontSize: 14,
            },
            legend: {
                display: false,
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

    get_data_book_per_month_statistics();

    function resize_data(size) {
        var data = data_per_month_in_time.slice();
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

    function save_data(data) {
        data_per_month_late = data['late'].slice();
        data_per_month_in_time = data['in_time'].slice();
        let chartData = {
            labels: generateLabels(),
            datasets: [{
                data: generateData('in_time'),
                backgroundColor: 'transparent',
                borderColor: colors[0],
                borderWidth: 2,
                pointBackgroundColor: colors[0],
            }, {
                data: generateData('late'),
                backgroundColor: 'transparent',
                borderColor: colors[1],
                borderWidth: 2,
                pointBackgroundColor: colors[1]
            }
            ]
        };
        create_line_chart(chartData);
    }

    function get_data_book_per_month_statistics() {
        $.ajax({
            type: "GET",
            url: "/statistics_book_per_month/",
            dataType: "json",
            success: function (data) {
                save_data(data['data'])
            }
        });
    }

});


