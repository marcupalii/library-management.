String.prototype.format = function () {
    let formatted = this;
    for (let arg in arguments) {
        formatted = formatted.replace("{" + arg + "}", arguments[arg]);
    }
    return formatted;
};

$(function () {

    $('#page_number')
        .css("display", "none")
        .val(1);
    $('#basic_page_number')
        .css("display", "none")
        .val(1);
    $('#basic_search_name').addClass("form-control mr-3 w-75");

    var nr_rows = 0;
    var data_form = "";
    var nr_of_pages = 1;


    function reset_err_tags() {
        $('#search_name_error').css("visibility", "hidden");
        $('.form-control').removeClass("has-error");
    }

    function write_row(row, row_index, book_id) {

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
                            .text(row['author_first_name'])
                            .attr("id", "author-first-name-row-content-" + row_index.toString())
                            .addClass("d-none d-md-block")
                    )
                    .append(
                        $('<td/>')
                            .text(row['author_last_name'])
                            .attr("id", "author-last-name-row-content-" + row_index.toString())
                            .addClass("d-none d-md-block")
                    )

                    .append(
                        $('<td/>')
                            .text(row['status'])
                            .addClass("d-none d-lg-block")
                            .attr("id", "status-book-row-content-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(book_id)
                            .attr("id", "book-id-row-content-" + row_index.toString())
                            .addClass("hidden-content")
                    )
                    .append(
                        $('<td/>')
                            .addClass("last-td")
                            .append(
                                $('<button/>')
                                    .addClass("btn accordion-toggle d-lg-none no-padding-button")
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
                                    .addClass("btn modal-button no-padding-button")
                                    .attr("id", row_index.toString())
                                    .attr("type", "button")
                                    .append(
                                        $('<i/>')
                                            .addClass("fas fa-external-link-alt")
                                    )
                            )
                    )
            )


            .append(
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
                                            .text("Author first name: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['author_first_name'])
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .addClass("d-md-none")
                                            .text("Author last name: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['author_last_name'])
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .addClass("d-lg-none")
                                            .text("Status : ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['status'])
                                            )
                                    )
                            )
                    )
            );
    }

    function show_page_numbers(page_numbers) {
        let pagination_container = $('#paginationBox');
        pagination_container.append(
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
                        pagination_container.append(
                            $('<li/>')
                                .addClass("page-item")
                                .html("...")
                        );
                    } else {
                        pagination_container.append(
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
                    pagination_container.append(
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
        pagination_container.append(
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

        if ($('#basic-search-container').hasClass('hide')) {
            $('#' + $('#page_number').val() + '.page-link').parent().addClass("active");
        } else {
            $('#' + $('#basic_page_number').val() + '.page-link').parent().addClass("active");

        }


    }


    function create_table(data) {
        let index_start = 1;
        let per_page = 15;
        if ($('#basic-search-container').hasClass('hide')) {
            index_start = per_page * (parseInt($('#page_number').val()) - 1);
        } else {
            index_start = per_page * (parseInt($('#basic_page_number').val()) - 1);
        }

        for (key in data['data']) {
            index_start += 1;
            write_row(data['data'][key], index_start, key);

        }
        if (index_start === 0) {
            $('#empty-results').css("visibility", "visible");
            $('#paginationBox').css("visibility", "hidden");
        } else {
            $('#empty-results').css("visibility", "hidden");
            $('#paginationBox').css("visibility", "visible");
        }

        $('#paginationBox').empty();
        if (index_start !== 0) {
            show_page_numbers(data['pages_lst']);
            if ($('#advanced-search-container').hasClass('hide')) {
                let page = $('#basic_page_number').val();
                $('#advanced-search-form').trigger('reset');
                $('#basic-search-form').trigger('reset');
                $('#basic_page_number').val(page);
            } else {
                let page = $('#page_number').val();
                $('#advanced-search-form').trigger('reset');
                $('#basic-search-form').trigger('reset');
                $('#page_number').val(page);
            }

        }
        if ($('#collapse-table').css("display") === "none") {
            $('#collapse-table').slideToggle(0);
        } else {
            $('#collapse-table')
                .slideToggle(0)
                .slideToggle(0);
        }
    }

    $.each($('input'), function () {
        if ($(this).attr("id").match(/^search_[a-z_]+$/) &&
            $(this).attr("id") !== "search_substring") {

            $(this).addClass("form-control");
            $(this).parent().prev().addClass("col-5 col-form-label");

        } else if ($(this).attr("id").match(/^exclude[a-z_]+$/) ||
            $(this).attr("id") === "search_substring" ||
            $(this).attr("id") === "only_available") {
            $(this).parent().prev().addClass("col-8 col-form-label");

        } else if ($(this).attr("id") === "days_number" || $(this).attr("id") === "rank") {
            $(this).css("width", "25%");
            $(this).addClass("form-control");

        }

    });

    function get_data() {
        $('#basic_search_name_error').css("visibility", "hidden");
        $('#basic_search_name').removeClass("has-error");

        if ($('#advanced-search-container').hasClass('hide')) {
            data_form = data_form.replace(/&basic_page_number=\d+&/, "&basic_page_number=" + $('#basic_page_number').val() + "&");
            $.ajax({
                type: "POST",
                url: "/basic_search_book/",
                data: data_form,
                success: function (data) {

                    // $('#basic-search-form').trigger('reset');
                    $('#content-table').empty();
                    if (data['data'].hasOwnProperty("basic_search_name")) {

                        if ($('#basic_search_name.form-control').hasClass('has-error') === false) {
                            $('#basic_search_name.form-control').addClass('has-error');
                        }

                        $('#basic_search_name_error')
                            .text(data['data']['basic_search_name']['0'])
                            .css("visibility", "visible");

                        if ($('#collapse-table').css("display") !== "none") {
                            $('#collapse-table').slideToggle(0);
                        }
                    } else {
                        create_table(data);
                    }
                }

            });
        } else {
            data_form = data_form.replace(/&page_number=\d+&/, "&page_number=" + $('#page_number').val() + "&");
            $.ajax({
                type: "POST",
                url: "/advanced_search_book/",
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

                        if ($('#search_author_first_name.form-control').hasClass('has-error') === false) {
                            $('#search_author_first_name.form-control').addClass('has-error');
                        }
                        if ($('#search_author_last_name.form-control').hasClass('has-error') === false) {
                            $('#search_author_last_name.form-control').addClass('has-error');
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

    }

    $('#basic-search-button').on('click', function (e) {
        $('#basic_page_number').val(1);
        data_form = $('#basic-search-form').serialize();
        get_data();
        e.preventDefault();
    });

    $('#advanced-search-button').on('click', function (e) {
        reset_err_tags();
        $('#page_number').val(1);
        data_form = $('#advanced-search-form').serialize();
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

        let page_nr = 0;
        if ($('#basic-search-container').hasClass('hide')) {
            page_nr = $('#page_number');
        } else {
            page_nr = $('#basic_page_number');
        }

        if ($(this).attr("id") === "prev") {
            if (parseInt(page_nr.val()) <= 1) {
                $(this).trigger("blur");
                return;
            }

            page_nr.val(parseInt(page_nr.val()) - 1);
        } else if ($(this).attr("id") === "next") {
            if (parseInt(page_nr.val()) >= nr_of_pages) {
                $(this).trigger("blur");
                return;
            }

            page_nr.val(parseInt(page_nr.val()) + 1);
        } else {
            page_nr.val(parseInt($(this).attr("id")));
        }
        get_data();
    });


    $('#days_number_error').css("visibility", "hidden");
    $('#rank_error').css("visibility", "hidden");
    $('#rank').css("width", "100%");
    $('#days_number').css("width", "100%");


    $('#add-to-wishlist-button').on('click', function () {

        let period_err = $('#days_number_error');
        let rank_err = $('#rank_error');

        period_err.css("visibility", "hidden");
        $('#rank').removeClass("has-error");
        $('#days_number').removeClass("has-error");

        rank_err.css("visibility", "hidden");
        $('#book_id').val($('#book-id').text());

        let rank = $('#rank').val();
        let rank_range = $('#rank-parent').contents().first().text().split("-");
        if (rank_range.length === 2) {
            if (parseInt(rank) < parseInt(rank_range[0].match(/[0-9]+/)[0]) ||
                parseInt(rank) > parseInt(rank_range[1].match(/[0-9]+/)[0])
            ) {
                rank_err
                    .css("visibility", "visible")
                    .text('Rank out of range');
                $('#rank').addClass("has-error");
                return
            }
        } else if (parseInt(rank) !== parseInt(rank_range[0].match(/[0-9]+/)[0])) {
            rank_err
                .css("visibility", "visible")
                .text('Rank out of range');
            $('#rank').addClass("has-error");
            return
        }


        $.ajax({
            type: "POST",
            url: "/add_to_wishlist/",
            data: $('#wishlist-form').serialize(),
            success: function (data) {
                if (data['data'].hasOwnProperty("days_number")) {
                    period_err
                        .css("visibility", "visible")
                        .text(data['data']["days_number"][0]);
                    $('#days_number').addClass("has-error");
                } else if (data['data'].hasOwnProperty("rank")) {
                    rank_err
                        .css("visibility", "visible")
                        .text(data['data']["rank"][0]);
                    $('#rank').addClass("has-error");
                } else {
                    $('#rank-parent').contents().first().remove();
                    $('#rank-parent').prepend("Range(1-{0})".format(data['data']));
                    $('#days_number').val('');
                    $('#rank').val('');
                    $('#myModal').modal('hide');
                }
                get_data();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#reserved-date-form').trigger('reset');
                $('#myModal').modal('hide');
                get_data();
            }
        });
    });

    $('#start_date_error').css("visibility", "hidden");
    $('#end_date_error').css("visibility", "hidden");

    $('#add-to-reserved-button').on('click', function () {
        $('#end_date').removeClass("has-error");
        $('#start_date').removeClass("has-error");
        $('#start_date_error').css("visibility", "hidden");
        $('#end_date_error').css("visibility", "hidden");

        $('#book_id_reserved').val($('#book-id').text());
        $.ajax({
            type: "POST",
            url: "/add_to_reserved/",
            data: $('#reserved-date-form').serialize(),
            success: function (data) {
                if (data['data'].hasOwnProperty("start_date")) {
                    $('#start_date_error')
                        .css("visibility", "visible")
                        .text(data['data']['start_date']);
                    $('#start_date').addClass("has-error");
                } else if (data['data'].hasOwnProperty("end_date")) {
                    $('#end_date_error')
                        .css("visibility", "visible")
                        .text(data['data']['end_date']);
                    $('#end_date').addClass("has-error");
                } else {
                    $('#reserved-date-form').trigger('reset');
                    $('#myModal').modal('hide');
                    get_data();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#reserved-date-form').trigger('reset');
                $('#myModal').modal('hide');
                get_data();
            }
        });
    });

    $('.search').on('click', function () {

        $('#collapse-table')
            .css("display", "none");
        $('#content-table').empty();
        $('#paginationBox').empty();

        if ($(this).attr("id") === "basic-search-change-container") {
            $('#basic-search-container').removeClass("hide");
            $('#advanced-search-container').addClass("hide");
        } else {
            $('#basic-search-container').addClass("hide");
            $('#advanced-search-container').removeClass("hide");
        }
    });

    $('#empty-results').css("visibility", "hidden");
    if ($('#content-table').children().length === 0) {
        $('#empty-results').css("visibility", "visible");
        $('#paginationBox').css("visibility", "hidden");
    }

    $(document).on("click", ".modal-button", function () {
        $('.wishlist-modal').css("visibility", "hidden");
        $('.reserved-modal').css("visibility", "hidden");
        $('#add-to-wishlist-button').css("visibility", "hidden");
        $('#add-to-reserved-button').css("visibility", "hidden");

        let id = $(this).attr("id");

        if ($("#status-book-row-content-" + id).text() === "Already in wishlist") {
            return redirect_to_wishlist_book($("#book-id-row-content-" + id).text());
        } else if ($("#status-book-row-content-" + id).text() === "Reserved") {
            return redirect_to_books_log($("#book-id-row-content-" + id).text());
        } else {

            if ($("#status-book-row-content-" + id).text() === "Unavailable") {
                $('.modal-title').text("Add book to wishlist");
                $('#add-to-wishlist-button').css("visibility", "visible");
                $('.wishlist-modal').css("visibility", "visible");
            } else {

                var currentdate = new Date();
                let year = currentdate.getFullYear();
                let month = currentdate.getMonth() + 1;
                if (month < 10) {
                    month = '0' + month
                }
                let day = currentdate.getDate();

                $('#start_date')
                    .attr("type", "date")
                    .attr("min", year + "-" + month + "-" + day)
                    .attr("max", year + "-" + month + "-" + day)
                    .addClass("form-control");

                $('#end_date')
                    .attr("type", "date")
                    .attr("min", year + "-" + month + "-" + day)
                    .attr("max", "2019-12-29")
                    .addClass("form-control");


                $('.reserved-modal').css("visibility", "visible");
                $('#add-to-reserved-button').css("visibility", "visible");
                $('.modal-title').text("Reserv the book");

            }

            $('#no').text($("#nr-row-content-" + id).text());
            $('#book-name').text($("#book-name-row-content-" + id).text());
            $('#book-type').text($("#book-type-row-content-" + id).text());
            $('#author-first-name').text($("#author-first-name-row-content-" + id).text());
            $('#author-last-name').text($("#author-last-name-row-content-" + id).text());
            $('#status').text($("#status-book-row-content-" + id).text());
            $('#book-id').text($("#book-id-row-content-" + id).text());
            $('#myModal').modal('toggle');
        }

    });

    function redirect_to_wishlist_book(book_id) {
        $.ajax({
            type: "GET",
            url: "/wishlist_book/" + book_id + "/",
            dataType: "json",
            success: function (data) {
                window.location = data["url"];
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#reserved-date-form').trigger('reset');
                $('#myModal').modal('hide');
                get_data();
            }

        });
    }

    function redirect_to_books_log(book_id) {
        $.ajax({
            type: "GET",
            url: "/reserved_book/" + book_id + "/",
            dataType: "json",
            success: function (data) {
                window.location = data["url"];
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#reserved-date-form').trigger('reset');
                $('#myModal').modal('hide');
                get_data();
            }
        });
    }


});

