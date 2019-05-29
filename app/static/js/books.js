$(document).ready(function () {

    $('#type_author-0').next().css("margin-bottom", "0");
    $('#type_author-1').next().css("margin-bottom", "0");
    $('#choose-author-container').addClass("d-none");

    $('.err-msg').each(function () {
        $(this).css("visibility", "hidden");
    });

    $('#type_author-0').on("click", function () {
        $('#choose-author-container').addClass("d-none");
        $('#author').val('');
    });

    $('#type_author-1').on("click", function () {
        $('#choose-author-container').removeClass("d-none");
        $('#author').val('');
    });


    $('#add-new-book-button').on("click", function (e) {
        e.preventDefault();
        $('.err-msg').each(function () {
            $(this).css("visibility", "hidden");
        });

        $.ajax({
            type: "POST",
            url: "/add_new_book/",
            data: $('#new-book-form').serialize(),
            success: function (data) {
                console.log(data['data']);
                if (data['data'].hasOwnProperty("id") === false) {
                    for (key in data['data']) {
                        $('#' + key + '_new_book_error')
                            .css("visibility", "visible")
                            .text(data['data'][key]);

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
        console.log("page_numbers=", page_numbers);
        let pagination_container = $('#paginationBox');
        pagination_container.empty();
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
        $('#author-result-container').removeClass("d-none");
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
                                .text(data['data'][id]['name'])
                                .attr("id", "author-first-name-row-content-" + row_index.toString())
                        )
                        .append(
                            $('<td/>')
                                .text(data['data'][id]['name'])
                                .attr("id", "author-last-name-row-content-" + row_index.toString())
                        )
                        .append(
                            $('<td/>')
                                .addClass("last-td")
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
                )
        }
        if (row_index === 0) {
            $('#empty-results').css("visibility", "visible");
            $('#paginationBox').css("visibility", "hidden");
        } else {

            $('#empty-results').css("visibility", "hidden");
            $('#paginationBox').css("visibility", "visible");
            show_pagination_buttons(data['pages_lst']);
        }

    }

    $('#page_nr').val(1);
    $('#empty-results').css("visibility", "hidden");
    var nr_of_pages = 1;
    var data_form = "";

    function get_authors() {
        $('#content-table').empty();
        $('#name_choose_author_error').css("visibility", "hidden");
        $('#author_name').removeClass("has-error");
        data_form = data_form.replace(/&page_nr=\d+&/, "&page_nr=" + $('#page_nr').val() + "&");
        console.log("data_Form in get authors=", data_form);
        $.ajax({
            type: "POST",
            url: "/choose_author/",
            data: data_form,
            success: function (data) {
                console.log(data['data']);
                if (data['data'].hasOwnProperty("author_name")) {
                    $('#author-result-container').addClass("d-none");
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
            page_nr.val(parseInt(page_nr.val()) <= 1 ? 1 : parseInt(page_nr.val()) - 1);
        } else if ($(this).attr("id") === "next") {
            page_nr.val(parseInt(page_nr.val()) >= nr_of_pages ? nr_of_pages : parseInt(page_nr.val()) + 1);
        } else {
            page_nr.val(parseInt($(this).attr("id")));
        }
        console.log("page_nr=", page_nr.val());
        get_authors();
    });

});