$(document).ready(function () {

    $('#type_author-0').next().css("margin-bottom", "0");
    $('#type_author-1').next().css("margin-bottom", "0");


    $('.err-msg').each(function () {
        $(this).css("visibility", "hidden");
    });

    $('#type_author-0').on("click", function () {

        if ($('#author-result-container').css("display") === "block") {
            $('#author-result-container').slideToggle(0);
        }
        if ($('#choose-author-container').css("display") === "block") {
            $('#choose-author-container').slideToggle(0);
        }
        $('#author').val('');
    });

    $('#type_author-1').on("click", function () {

        let author_container = $('#choose-author-container');
        if (author_container.css("display") === "none") {
            author_container.slideToggle(0);
        }

        $('#author').val('');
    });


    $(document).on("click", '#type_exists-0', function () {

        if ($('#type_string').hasClass("display-none") === false) {
            $('#type_string').addClass("display-none");
        }
        if ($('#type_select').hasClass("display-none")) {
            $('#type_select').removeClass("display-none");
        }

        $('#type').val('');
        $('#type_string_field').val('');

    });

    $(document).on("click", '#type_exists-1', function () {

        if ($('#type_select').hasClass("display-none") === false) {
            $('#type_select').addClass("display-none");
        }
        $('#type_string').removeClass("display-none");
        $('#type').val('');
        $('#type_string_field').val('');
    });

    $('#name').on("change", function () {
        $('#name').removeClass("has-error");
        $('#name_new_book_error').css("visibility", "hidden");
    });

    $('#type').on("change", function () {
        $('#type').removeClass("has-error");
        $('#type_new_book_error').css("visibility", "hidden");
    });

    $('#author_first_name').on("change", function () {
        $('#author_first_name').removeClass("has-error");
        $('#author_first_name_new_book_error').css("visibility", "hidden");
    });

    $('#author_last_name').on("change", function () {
        $('#author_last_name').removeClass("has-error");
        $('#author_last_name_new_book_error').css("visibility", "hidden");
    });

    $('#series').on("change", function () {
        $('#series').removeClass("has-error");
        $('#series_new_book_error').css("visibility", "hidden");
    });

    $('#add-new-book-button').on("click", function (e) {
        e.preventDefault();

        $('#name').removeClass("has-error");
        $('#type').removeClass("has-error");
        $('#author_first_name').removeClass("has-error");
        $('#author_last_name').removeClass("has-error");
        $('#series').removeClass("has-error");

        $('.err-msg').each(function () {
            $(this).css("visibility", "hidden");
        });
        $.ajax({
            type: "POST",
            url: "/add_new_book/",
            data: $('#new-book-form').serialize(),
            success: function (data) {

                if (data['data'].hasOwnProperty("id") === false) {
                    for (key in data['data']) {
                        $('#' + key + '_new_book_error')
                            .css("visibility", "visible")
                            .text(data['data'][key]);
                        $('#' + key).addClass("has-error");
                    }
                } else {
                    $('.err-msg').each(function () {
                        $(this).css("visibility", "hidden");
                    });
                    $('#new-book-form').trigger("reset");
                }
            }
        });
    });

    function show_pagination_buttons(page_numbers) {
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
        $('#' + $('#page_nr').val() + '.page-link').parent().addClass("active");
    }

    function write_data(data) {
        let per_page = 3;
        let row_index = per_page * (parseInt($('#page_nr').val()) - 1);
        $('#content-table').empty();
        for (let id in data['data']) {
            row_index += 1;

            $('#content-table')
                .append(
                    $('<tr/>')
                        .attr("colspan", "4")
                        .append(
                            $('<td/>')
                                .text(row_index.toString())
                                .attr("id", "nr-row-content-" + row_index.toString())
                        )
                        .append(
                            $('<td/>')
                                .text(data['data'][id]['first_name'])
                                .attr("id", "author-first-name-row-content-" + row_index.toString())
                        )
                        .append(
                            $('<td/>')
                                .text(data['data'][id]['last_name'])
                                .attr("id", "author-last-name-row-content-" + row_index.toString())
                        )
                        .append(
                            $('<td/>')
                                .append(
                                    $('<button/>')
                                        .addClass("btn select-author-button")
                                        .attr("id", row_index.toString())
                                        .attr("type", "button")
                                        .append(
                                            $('<i/>')
                                                .addClass("fas fa-external-link-alt")
                                        )
                                )
                        )
                )
        }
        if ($('#author-result-container').css("display") === "none") {
            $('#author-result-container').slideToggle(0);
        }
        if (row_index === 0) {
            $('#empty-results').css("visibility", "visible");
            $('#paginationBox')
                .css("visibility", "hidden")
                .empty();
        } else {

            $('#empty-results').css("visibility", "hidden");
            $('#paginationBox')
                .css("visibility", "visible")
                .empty();
            show_pagination_buttons(data['pages_lst']);
        }

    }

    $('#page_nr').val(1);
    $('#empty-results').css("visibility", "hidden");
    var nr_of_pages = 1;
    var data_form = "";

    function get_authors() {

        $('#name_choose_author_error').css("visibility", "hidden");
        $('#author_name').removeClass("has-error");
        data_form = data_form.replace(/&page_nr=\d+&/, "&page_nr=" + $('#page_nr').val() + "&");
        $.ajax({
            type: "POST",
            url: "/choose_author/",
            data: data_form,
            success: function (data) {

                if (data['data'].hasOwnProperty("author_name")) {
                    $('#author-result-container').slideToggle(0);
                    $('#name_choose_author_error')
                        .css("visibility", "visible")
                        .text(data['data']["author_name"]);
                    $('#author_name').addClass("has-error");
                } else {
                    $('#name_choose_author_error').css("visibility", "hidden");
                    $('#author_name').val('');
                    write_data(data);
                }
            }
        });
    }

    $('#search-author-button').on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        data_form = $('#choose-author-form').serialize();
        get_authors();
    });

    $(document).on("click", ".page_num_link", function () {

        let page_nr = $('#page_nr');

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
        get_authors();
    });
    $(document).on("click", ".select-author-button", function () {
        $('#author_first_name').val(
            $('#author-first-name-row-content-' + $(this).attr("id")).text()
        );
        $('#author_last_name').val(
            $('#author-last-name-row-content-' + $(this).attr("id")).text()
        );
        // $(this).trigger("blur");
    });


    // #####################################################
    // #####################################################
    // #####################################################
    // #####################################################
    var nr_of_pages_search_books = 1;
    $('#advance-search-change-container').on("click", function () {
        $("#basic-search-container").addClass("d-none");
        $("#advanced-search-container").removeClass("d-none");
    });
    $('#basic-search-change-container').on("click", function () {
        $('#advanced-search-container').addClass("d-none");
        $("#basic-search-container").removeClass("d-none");
    });

    function write_row(row, row_index, book_series) {
        $('#content-table-search-books')
            .append(
                $('<tr/>')
                    .attr("colspan", "7")
                    .append(
                        $('<td/>')
                            .text(row_index.toString())
                            .attr("id", "nr-row-content-search-books-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['book_name'])
                            .attr("id", "book-name-row-content-search-books-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['book_type'])
                            .attr("id", "book-type-row-content-search-books-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['book_series'])
                            .attr("id", "book-series-row-content-search-books-" + row_index.toString())
                    )

                    .append(
                        $('<td/>')
                            .text(row['author_first_name'])
                            .attr("id", "author-first-name-row-content-search-books-" + row_index.toString())
                            .addClass("d-none d-md-block")
                    )
                    .append(
                        $('<td/>')
                            .text(row['author_last_name'])
                            .attr("id", "author-last-name-row-content-search-books-" + row_index.toString())
                            .addClass("d-none d-md-block")
                    )

                    .append(
                        $('<td/>')
                            .text(row['status'])
                            .addClass("d-none d-lg-block")
                            .attr("id", "status-book-row-content-search-books-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(book_series)
                            .attr("id", "series-id-row-content-search-books-" + row_index.toString())
                            .addClass("hidden-content")
                    )
                    .append(
                        $('<td/>')
                            .addClass("last-td")
                            .append(
                                $('<button/>')
                                    .addClass("btn accordion-toggle d-lg-none")
                                    .attr("data-toggle", "collapse")
                                    .attr("data-target", "#tr-collapse-id-search-books-" + row_index.toString())
                                    .attr("aria-controls", "aria-controls-search-books-" + row_index.toString())
                                    .attr("id", "search-books-" + row_index.toString())
                                    .attr("type", "button")
                                    .append(
                                        $('<i/>')
                                            .addClass("fas fa-expand-arrows-alt")
                                    )
                            )
                            .append(
                                $('<button/>')
                                    .addClass("btn edit-search-books-button")
                                    .attr("id", row_index.toString())
                                    .attr("type", "button")
                                    .append(
                                        $('<i/>')
                                            .addClass("far fa-edit")
                                    )
                            )
                    )
            )
            .append(
                $('<tr/>')
                    .addClass("sub-table-row p collapse p-3 tr-collapse-search-books-" + row_index.toString())
                    .attr("id", "tr-collapse-id-search-books-" + row_index.toString())
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
        let pagination_container = $('#paginationBox-search-books');
        pagination_container.append(
            $('<li/>')
                .addClass("page-item")
                .append(
                    $('<button/>')
                        .attr("id", "prev-search-books")
                        .addClass("btn btn-secondary page_num_link_search_books page-link")
                        .html("&laquo;")
                )
        );
        for (var i = 0; i < page_numbers.length; i++) {
            if (page_numbers[i] !== null) {
                nr_of_pages_search_books = page_numbers[i];
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
                                        .addClass("btn btn-secondary page_num_link_search_books page-link")
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
                                    .addClass("btn btn-secondary page_num_link_search_books page-link")
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
                        .attr("id", "next-search-books")
                        .addClass("btn btn-secondary page_num_link_search_books page-link")
                        .html("&raquo;")
                )
        );
        $('.page-link').parent().removeClass("active");

        if ($('#basic-search-container').hasClass('d-none')) {
            $('#' + $('#page_number').val() + '.page-link').parent().addClass("active");
        } else {
            $('#' + $('#basic_page_number').val() + '.page-link').parent().addClass("active");

        }


    }

    function create_table(data) {
        let index_start = 1;
        let per_page = 15;
        if ($('#basic-search-container').hasClass('d-none')) {
            index_start = per_page * (parseInt($('#page_number').val()) - 1);
        } else {
            index_start = per_page * (parseInt($('#basic_page_number').val()) - 1);
        }
        for (key in data['data']) {
            index_start += 1;
            write_row(data['data'][key], index_start, key);

        }
        if (index_start === 0) {
            $('#empty-results-search-books').css("visibility", "visible");
            $('#paginationBox-search-books').css("visibility", "hidden");
        } else {
            $('#empty-results-search-books').css("visibility", "hidden");
            $('#paginationBox-search-books').css("visibility", "visible");
        }

        $('#paginationBox-search-books').empty();
        if (index_start !== 0) {
            show_page_numbers(data['pages_lst']);
            if ($('#advanced-search-container').hasClass('d-none')) {
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
        if ($('#collapse-table-search-books').css("display") === "none") {
            $('#collapse-table-search-books').slideToggle(0);
        } else {
            $('#collapse-table-search-books')
                .slideToggle(0)
                .slideToggle(0);
        }
    }

    function get_data() {
        $('#basic_search_name_error').css("visibility", "hidden");
        $('#basic_search_name').removeClass("has-error");
        if ($('#advanced-search-container').hasClass('d-none')) {
            data_form = data_form.replace(/&basic_page_number=\d+&/, "&basic_page_number=" + $('#basic_page_number').val() + "&");
            $.ajax({
                type: "POST",
                url: "/admin_dashboard_basic_search_book/",
                data: data_form,
                success: function (data) {

                    // $('#basic-search-form').trigger('reset');
                    $('#content-table-search-books').empty();
                    if (data['data'].hasOwnProperty("basic_search_name")) {

                        if ($('#basic_search_name.form-control').hasClass('has-error') === false) {
                            $('#basic_search_name.form-control').addClass('has-error');
                        }

                        $('#basic_search_name_error')
                            .text(data['data']['basic_search_name']['0'])
                            .css("visibility", "visible");

                        if ($('#collapse-table-search-books').css("display") !== "none") {
                            $('#collapse-table-search-books').slideToggle(0);
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
                url: "/admin_dashboard_advanced_search_book/",
                data: data_form,
                success: function (data) {
                    $('#content-table-search-books').empty();

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

                        if ($('#collapse-table-search-books').css("display") !== "none") {
                            $('#collapse-table-search-books').slideToggle(0);
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
        $('#page_number').val(1);
        data_form = $('#advanced-search-form').serialize();
        get_data();
        e.preventDefault();
    });

    $(document).on("click", ".page_num_link_search_books", function () {

        let page_nr = 0;
        if ($('#basic-search-container').hasClass('d-none')) {
            page_nr = $('#page_number');
        } else {
            page_nr = $('#basic_page_number');
        }

        if ($(this).attr("id") === "prev-search-books") {
            if (parseInt(page_nr.val()) <= 1) {
                $(this).trigger("blur");
                return;
            }

            page_nr.val(parseInt(page_nr.val()) - 1);
        } else if ($(this).attr("id") === "next-search-books") {
            if (parseInt(page_nr.val()) >= nr_of_pages_search_books) {
                $(this).trigger("blur");
                return;
            }

            page_nr.val(parseInt(page_nr.val()) + 1);
        } else {
            page_nr.val(parseInt($(this).attr("id")));
        }
        get_data();
    });

    $('#empty-results-search-books').css("display", "hidden");
    if ($('#content-table-search-books').children().length === 0) {
        $('#empty-results-search-books').css("visibility", "visible");
        $('#paginationBox-search-books').css("visibility", "hidden");
    }
    $('#basic_search_name').val("all");
    $('#basic-search-button').trigger('click');

    $(document).on("click", '.edit-search-books-button', function () {

        $('#update-book-modal').modal('show');
        let row_id = $(this).attr("id");
        let status = $('#status-book-row-content-search-books-' + row_id).text();
        $('#update_book_series_id').val($('#series-id-row-content-search-books-' + row_id).text());
        if (status === "available") {
            $('#update_book_name')
                .val($('#book-name-row-content-search-books-' + row_id).text())
                .prop("disabled", false);
            $('#update_book_type')
                .val($('#book-type-row-content-search-books-' + row_id).text())
                .prop("disabled", false);
            $('#update_book_series')
                .val($('#book-series-row-content-search-books-' + row_id).text())
                .prop("disabled", false);
            $('#update_author_first_name')
                .val($('#author-first-name-row-content-search-books-' + row_id).text())
                .prop("disabled", false);
            $('#update_author_last_name')
                .val($('#author-last-name-row-content-search-books-' + row_id).text())
                .prop("disabled", false);
            $('#delete-book-button').removeClass("disabled");
            $('#update-book-button').removeClass("disabled");

        } else {
            if ($('#delete-book-button').hasClass("disabled") === false) {
                $('#delete-book-button').addClass("disabled");
            }
            if ($('#update-book-button').hasClass("disabled") === false) {
                $('#update-book-button').addClass("disabled");
            }

            $('#update_book_name')
                .val($('#book-name-row-content-search-books-' + row_id).text())
                .prop("disabled", "true")
            $('#update_book_type')
                .val($('#book-type-row-content-search-books-' + row_id).text())
                .prop("disabled", "true");
            $('#update_book_series')
                .val($('#book-series-row-content-search-books-' + row_id).text())
                .prop("disabled", "true");
            $('#update_author_first_name')
                .val($('#author-first-name-row-content-search-books-' + row_id).text())
                .prop("disabled", "true");
            $('#update_author_last_name')
                .val($('#author-last-name-row-content-search-books-' + row_id).text())
                .prop("disabled", "true");
        }
        if (status == "taken") {
            $('#msg-rent').text("");
            $('#title-rent').text("");
            $.ajax({
                type: "GET",
                url: "/get_user_taken_book/" + $('#update_book_series_id').val() + "/",
                success: function (data) {
                    console.log(data['data']);
                    // $('#update-book-modal').modal('hide');
                    // get_data();
                    $('#rent-book-container').removeClass("d-none");
                    for (let key in data['data']) {
                        $('#' + key + '_rent').text(data['data'][key]);
                    }
                    if (data['data'['user_entry_status']] == "Reserved") {
                        $('#msg-rent').text(
                            "Are you sure you want to rent the book?"
                        );
                        $('#title-rent').text("Rent the book")
                    } else {
                        $('#msg-rent').text(
                            "Are you sure you want to receive the book?"
                        );
                        $('#title-rent').text("Receive the book")
                    }

                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR);
                    console.log(textStatus);
                    console.log(errorThrown);
                    $('#update-book-modal').modal('hide');
                    get_data();
                }
            });
        }
    });
    $(document).on("click", '#rent-book-button', function () {
        $.ajax({
            type: "GET",
            url: "/rent_book/" + $('#update_book_series_id').val() + "/",
            success: function (data) {
                console.log(data['data']);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#update-book-modal').modal('hide');
                get_data();
            }
        });

    });
    $('#update-book-button').on("click", function (e) {
        e.preventDefault();
        $('#update_book_name').removeClass("has-error");
        $('#update_book_type').removeClass("has-error");
        $('#update_book_series').removeClass("has-error");
        $('#update_author_first_name').removeClass("has-error");
        $('#update_author_last_name').removeClass("has-error");
        if ($('#update_book_series').prop("disabled") == true) {
            $('#update-book-modal').modal('hide');
            return;
        }
        $.ajax({
            type: "POST",
            url: "/update_book/",
            data: $('#update-book-form').serialize(),
            success: function (data) {
                console.log(data['data']);
                if (data['data'].hasOwnProperty("id") === false) {
                    for (key in data['data']) {
                        $('#' + key + '_update_book_error')
                            .css("visibility", "visible")
                            .text(data['data'][key]);
                        $('#' + key).addClass("has-error");
                    }
                } else {
                    $('.err-msg').each(function () {
                        $(this).css("visibility", "hidden");
                    });
                    $('#new-book-form').trigger("reset");
                    $('#update-book-modal').modal('hide');
                }
            }
        });
    });
    $(document).on("click", '#close-update-book-modal', function () {
        $('#update_book_name').removeClass("has-error");
        $('#update_book_type').removeClass("has-error");
        $('#update_book_series').removeClass("has-error");
        $('#update_author_first_name').removeClass("has-error");
        $('#update_author_last_name').removeClass("has-error");
        $('.err-msg').each(function () {
            $(this).css("visibility", "hidden");
        });
    });
    $('#only_unreturned').on("click", function () {
        $('#only_available').prop("checked", false);
    });
    $('#only_available').on("click", function () {
        $('#only_unreturned').prop("checked", false);
    });

    $(document).on('click', '#delete-book-button', function (e) {
        if ($(this).hasClass("disabled")) {
            e.stopPropagation();
            e.preventDefault();
            $('#update-book-modal').modal('hide');
            return;
        }
        $.ajax({
            type: "DELETE",
            url: "/delete_book_series/" + $('#update_book_series_id').val() + "/",
            success: function (data) {
                console.log(data['data']);
                $('#update-book-modal').modal('hide');
                get_data();
            }
        });
    });
});