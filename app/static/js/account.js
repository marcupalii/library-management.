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
        labels: ["Jan", "Feb","Mar", "Apr", "May", "June", "July","Aug","Sept","Oct","Nov","Dec"],
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


    $('#option-0').prop('checked', true);

    function get_autocomplete(option) {
        $.ajax({
            url: "/autocomplete/" + option + "/",
            type: 'GET',
            contentType: 'application/json;charset=UTF-8',
        }).done(function (data) {
            console.log(data);
            $('#name_autocomplete').autocomplete({
                minLength: 1,
                source: function (req, resp) {
                    var match = new RegExp("^" + $.ui.autocomplete.escapeRegex(req.term), "i");
                    resp($.grep(data, function (el) {
                        return match.test(el);
                    }));
                }
            });
        });
    }

    get_autocomplete("1");

    $(document).on('change', 'input:radio[id^="option-"]', function () {
        get_autocomplete($(this)[0].value);
    });

    function reset_err_tags() {
        $('#name-err').css("visibility", "hidden");
        if ($('#name_autocomplete').hasClass('has-error')) {
            $('#name_autocomplete').toggleClass('has-error');
        }
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

        console.log("nr_of_pages" + nr_of_pages);
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
        for (key in data['data']) {
            nr_rows += 1;
            write_row(data['data'][key], nr_rows);
        }
        show_page_numbers(data['pages_lst']);
        if (nr_rows === 0) {
            $('#content-table').css("text-align", "center").text("no results find !");
        }

        if ($('#collapse-table').css("display") === "none") {

            $('#collapse-table').slideToggle(0);
        } else {
            $('#collapse-table').slideToggle(0);
            $('#collapse-table').slideToggle(0);
        }
    }

    function get_data() {

        data_form = data_form.replace(/&page_number=\d+&/, "&page_number=" + $('#page_number').val() + "&");
        $.ajax({
            type: "POST",
            url: "/process_search_form/",
            data: data_form,
            success: function (data) {

                $('#name_autocomplete').val('');
                $('#content-table').empty();

                if (data['data'].hasOwnProperty("autocomp")) {
                    if ($('#name_autocomplete').hasClass('has-error') === false) {
                        $('#name_autocomplete').addClass('has-error');
                    }

                    $('#name-err').text(data['data']['autocomp']['0']);
                    $('#name-err').css("visibility", "visible");

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


    $.extend($.ui.autocomplete.prototype.options, {

        open: function (event, ui) {

            if ($('#name_autocomplete').val() !== "") {
                $('#name-err').css("visibility", "hidden");
                if ($('#name_autocomplete').hasClass('has-error')) {
                    $('#name_autocomplete').toggleClass('has-error');
                }
            }


            $(".selector").autocomplete({autoFocus: true});
            $(this).autocomplete("widget").css({
                "width": ($('#search-container').width() + "px")
            });

            $('.ui-menu-item').css("width", "99%");

            $('.ui-menu-item').css("margin-left", "1.5px");

        }
        ,
    })
    ;

    $(window).resize(function () {
        $(".ui-menu").css({"display": "none"});
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
        console.log("page_nr.val()=" + page_nr.val());
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
