$(function () {


    var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];

    /* 3 donut charts */
    var donutOptions = {
        cutoutPercentage: 85,
        legend: {position: 'bottom', padding: 5, labels: {pointStyle: 'circle', usePointStyle: true}}
    };

// donut 1
    var chDonutData1 = {
        labels: ['Science', 'Literature', 'Other'],
        datasets: [
            {
                backgroundColor: colors.slice(0, 3),
                borderWidth: 0,
                data: [74, 11, 40]
            }
        ]
    };

    var chDonut1 = document.getElementById("chDonut1");
    if (chDonut1) {
        new Chart(chDonut1, {
            type: 'pie',
            data: chDonutData1,
            options: donutOptions
        });
    }

// donut 2
    var chDonutData2 = {
        labels: ['Science', 'Literature', 'Other'],
        datasets: [
            {
                backgroundColor: colors.slice(0, 3),
                borderWidth: 0,
                data: [40, 45, 30]
            }
        ]
    };
    var chDonut2 = document.getElementById("chDonut2");
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
    if (chDonut3) {
        new Chart(chDonut3, {
            type: 'pie',
            data: chDonutData3,
            options: donutOptions
        });
    }


    var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];

    /* large line chart */
    var chLine = document.getElementById("chLine");
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

    if (chLine) {
        new Chart(chLine, {
            type: 'line',
            data: chartData,
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                },
                legend: {
                    display: false
                }
            }
        });
    }


    $('#page_number').css("display", "none");
    $('#page_number').val(1);
    var nr_rows = 0;
    var data_form = "";
    var nr_of_pages = 1;
    $('.accordion-toggle').click(function () {

        // if ($('.accordion-toggle').attr('aria-expanded') === "true") {
        //     $('.accordion-toggle').attr('aria-expanded', "false");
        // }
        // if ($('.accordion-toggle').hasClass('collapsed') === "false") {
        //     $('.accordion-toggle').addClass('collapsed');
        // }
        // if ($('.sub-table-row').hasClass("show")) {
        //     $('.sub-table-row').removeClass("show");
        // }
        //
        // $('.hiddenRow').hide();

        $(this).next('tr').find('.hiddenRow').show();
    });


    function reset_err_tags() {
        $('#search_name_error').css("visibility", "hidden");
        $('.form-control').removeClass("has-error");
    }


    function write_row(row, row_index) {

        $('#content-table')
            .append(
                $('<tr/>')
                    .attr("colspan", "6")
                    .append(
                        $('<td/>')
                            .text(row_index.toString())
                            .attr("id", "nr-row-content-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['book_name'])
                            .attr("id", "book-name-row-content-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['book_type'])
                            .attr("id", "book-type-row-content-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['author_name'])
                            .attr("id", "author-name-row-content-" + row_index.toString())
                            .addClass("d-none d-md-block")
                    )

                    .append(
                        $('<td/>')
                            .text(row['count_book'])
                            .addClass("d-none d-lg-block")
                            .attr("id", "count-book-row-content-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .append(
                                $('<button/>')
                                    .addClass("btn accordion-toggle d-lg-none")
                                    .attr("data-toggle", "collapse")
                                    .attr("data-target", "#tr-collapse-id-" + row_index.toString())
                                    .attr("aria-controls", "aria-controls" + row_index.toString())
                                    .attr("id", row_index.toString())
                                    .attr("type", "button")
                                    .append(
                                        $('<i/>')
                                            .addClass("fas fa-expand-arrows-alt")
                                    )
                            )
                            .append(
                                $('<button/>')
                                    .addClass("btn modal-button")
                                    .attr("id", row_index.toString())
                                    .attr("type", "button")
                                    .append(
                                        $('<i/>')
                                            .addClass("fas fa-external-link-alt")
                                    )
                            )
                    )
            );


        $('#content-table').append(
            $('<tr/>')
                .addClass("sub-table-row p collapse p-3 tr-collapse-" + row_index.toString())
                .attr("id", "tr-collapse-id-" + row_index.toString())
                .append(
                    $('<td/>')
                        .attr("colspan", "6")
                        .addClass("hiddenRow")
                        .append(
                            $('<div/>')
                                .addClass("accordian-body")
                                .append(
                                    $('<p/>')
                                        .addClass("d-md-none")
                                        .text("author_name: ")
                                        .append(
                                            $('<span/>')
                                                .text(row['author_name'])
                                        )
                                )
                                .append(
                                    $('<p/>')
                                        .addClass("d-lg-none")
                                        .text("Status : ")
                                        .append(
                                            $('<span/>')
                                                .text(row['count_book'])
                                        )
                                )
                        )
                )
        );
    }

    function show_page_numbers(page_numbers) {
        $('#paginationBox').empty();
        $('#paginationBox').append(
            $('<li/>')
                .addClass("page-item")
                .append(
                    $('<button/>')
                        .attr("id", "prev")
                        .addClass("btn btn-secondary page_num_link page-link")
                        .html("&laquo;")
                )
        );
        for (var i = 0; i < page_numbers.length; i++) {
            if (page_numbers[i] !== null) {
                nr_of_pages = page_numbers[i];
                if (i !== 0) {
                    if (page_numbers[i - 1] !== page_numbers[i] - 1) {
                        $('#paginationBox').append(
                            $('<li/>')
                                .addClass("page-item")
                                .html("...")
                        );
                    } else {
                        $('#paginationBox').append(
                            $('<li/>')
                                .addClass("page-item")
                                .append(
                                    $('<button/>')
                                        .attr("id", page_numbers[i])
                                        .addClass("btn btn-secondary page_num_link page-link")
                                        .html(page_numbers[i] + "  ")
                                )
                        );
                    }
                } else {
                    $('#paginationBox').append(
                        $('<li/>')
                            .addClass("page-item")
                            .append(
                                $('<button/>')
                                    .attr("id", page_numbers[i])
                                    .addClass("btn btn-secondary page_num_link page-link")
                                    .html(page_numbers[i] + "  ")
                            )
                    );
                }
            }

        }
        $('#paginationBox').append(
            $('<li/>')
                .addClass("page-item")
                .append(
                    $('<button/>')
                        .attr("id", "next")
                        .addClass("btn btn-secondary page_num_link page-link")
                        .html("&raquo;")
                )
        );
        $('.page-link').parent().removeClass("active");
        $('#' + $('#page_number').val() + '.page-link').parent().addClass("active");

    }

    function create_table(data) {
        let index_start = 3 * (parseInt($('#page_number').val()) - 1);
        for (key in data['data']) {
            index_start += 1;
            write_row(data['data'][key], index_start);

        }
        if (index_start !== 0) {
            show_page_numbers(data['pages_lst']);
        } else {
            $('#content-table').css("text-align", "center").text("no results find !");
        }

        if ($('#collapse-table').css("display") === "none") {
            $('#collapse-table').slideToggle(0);
        } else {
            $('#collapse-table').slideToggle(0);
            $('#collapse-table').slideToggle(0);
        }
    }

    $.each($('input'), function () {
        if ($(this).attr("id").match(/^search_[a-z]+$/)) {
            $(this).addClass("form-control");
            $(this).parent().prev().addClass("col-sm-2 col-form-label");
        }
    });

    function get_data() {
        data_form = data_form.replace(/&page_number=\d+&/, "&page_number=" + $('#page_number').val() + "&");
        $.ajax({
            type: "POST",
            url: "/search_book/",
            data: data_form,
            success: function (data) {
                $('#content-table').empty();

                if (data['data'].hasOwnProperty("search_name")) {

                    if ($('#search_name.form-control').hasClass('has-error') === false) {
                        $('#search_name.form-control').addClass('has-error');
                    }

                    if ($('#search_type.form-control').hasClass('has-error') === false) {
                        $('#search_type.form-control').addClass('has-error');
                    }

                    if ($('#search_author.form-control').hasClass('has-error') === false) {
                        $('#search_author.form-control').addClass('has-error');
                    }


                    $('#search_name_error').text(data['data']['search_name']['0']);
                    $('#search_name_error').css("visibility", "visible");

                    if ($('#collapse-table').css("display") !== "none") {
                        $('#collapse-table').slideToggle(0);
                    }
                } else {
                    create_table(data);
                }
            }

        });
    }


    $('form').submit(function (e) {
        reset_err_tags();
        data_form = $('form').serialize();
        get_data();
        e.preventDefault();
    });


    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    });


    $(document).on("click", ".page_num_link", function () {

        let page_nr = $('#page_number');

        if ($(this).attr("id") === "prev") {
            page_nr.val(parseInt(page_nr.val()) <= 1 ? 1 : parseInt(page_nr.val()) - 1);
        } else if ($(this).attr("id") === "next") {
            page_nr.val(parseInt(page_nr.val()) >= nr_of_pages ? nr_of_pages : parseInt(page_nr.val()) + 1);
        } else {
            page_nr.val(parseInt($(this).attr("id")));
        }
        get_data();
    });

});


$(document).on("click", ".modal-button", function () {
    let id = $(this).attr("id");
    $('#no').text($("#nr-row-content-" + id).text());
    $('#book-name').text($("#book-name-row-content-" + id).text());
    $('#book-type').text($("#book-type-row-content-" + id).text());
    $('#author-name').text($("#author-name-row-content-" + id).text());
    $('#status').text($("#count-book-row-content-" + id).text());

    $('#myModal').modal('toggle');
});
