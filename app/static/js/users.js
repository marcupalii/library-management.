$(function () {
    $('#file').on('change', function () {
        let count = $(this).val().split('\\').length;
        $(this).next('.custom-file-label').html($(this).val().split('\\')[count - 1]);
    });
    $.each($('.form-control'), function () {
        if ($(this).parent().next('.err-msg').text() !== "") {
            $(this).addClass("has-error");
        }
    });
    if ($('#first_name_new_user_error').text() !== "") {
        $('#file').addClass("has-error");
    }

    var data_form = "";
    var nr_of_pages_search_users = 1;
    $('#advance-search-change-container').on("click", function () {
        $("#basic-search-container").addClass("d-none");
        $("#advanced-search-container").removeClass("d-none");
    });
    $('#basic-search-change-container').on("click", function () {
        $('#advanced-search-container').addClass("d-none");
        $("#basic-search-container").removeClass("d-none");
    });


    function write_row(row, row_index, user_id) {
        $('#content-table-search-users')
            .append(
                $('<tr/>')
                    .attr("colspan", "7")
                    .append(
                        $('<td/>')
                            .text(row_index.toString())
                            .attr("id", "nr-row-content-search-users-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['user_first_name'])
                            .attr("id", "user-first-name-row-content-search-users-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['user_last_name'])
                            .attr("id", "user-last-name-row-content-search-users-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['user_library_card_id'])
                            .addClass("d-none d-md-block")
                            .attr("id", "user-library-card-id-row-content-search-users-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['user_type'])
                            .addClass("d-none d-md-block")
                            .attr("id", "user-type-row-content-search-users-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(row['user_email'])
                            .addClass("d-none d-lg-block")
                            .attr("id", "user-email-row-content-search-users-" + row_index.toString())
                    )
                    .append(
                        $('<td/>')
                            .text(user_id)
                            .attr("id", "user-id-row-content-search-users-" + row_index.toString())
                            .addClass("hidden-content")
                    )
                    .append(
                        $('<td/>')
                            .addClass("last-td")
                            .append(
                                $('<button/>')
                                    .addClass("btn accordion-toggle")
                                    .attr("data-toggle", "collapse")
                                    .attr("data-target", "#tr-collapse-id-search-users-" + row_index.toString())
                                    .attr("aria-controls", "aria-controls-search-users-" + row_index.toString())
                                    .attr("id", "search-users-" + row_index.toString())
                                    .attr("type", "button")
                                    .append(
                                        $('<i/>')
                                            .addClass("fas fa-expand-arrows-alt")
                                    )
                            )
                            .append(
                                $('<button/>')
                                    .addClass("btn edit-search-users-button")
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
                    .addClass("sub-table-row p collapse p-3 tr-collapse-search-users-" + row_index.toString())
                    .attr("id", "tr-collapse-id-search-users-" + row_index.toString())
                    .append(
                        $('<td/>')
                            .attr("colspan", "7")
                            .addClass("hiddenRow")
                            .append(
                                $('<div/>')
                                    .addClass("accordian-body")
                                    .append(
                                        $('<p/>')
                                            .text("User`s return book  coefficient: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_trust_coeff'])
                                                    .attr("id", "user-trust-coeff-row-content-search-users-" + row_index.toString())
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .text("User address: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_address'])
                                                    .attr("id", "user-address-row-content-search-users-" + row_index.toString())
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .text("User city: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_city'])
                                                    .attr("id", "user-city-row-content-search-users-" + row_index.toString())
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .text("User country: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_country'])
                                                    .attr("id", "user-country-row-content-search-users-" + row_index.toString())
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .text("User zip code: ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_zip_code'])
                                                    .attr("id", "user-zip-code-row-content-search-users-" + row_index.toString())
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .addClass("d-md-none")
                                            .text("Status : ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_library_card_id'])
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .addClass("d-md-none")
                                            .text("Status : ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_type'])
                                            )
                                    )
                                    .append(
                                        $('<p/>')
                                            .addClass("d-lg-none")
                                            .text("Status : ")
                                            .append(
                                                $('<span/>')
                                                    .text(row['user_email'])
                                            )
                                    )
                            )
                    )
            );
    }

    function show_page_numbers(page_numbers) {
        let pagination_container = $('#paginationBox-search-users');
        pagination_container.append(
            $('<li/>')
                .addClass("page-item")
                .append(
                    $('<button/>')
                        .attr("id", "prev-search-users")
                        .addClass("btn btn-secondary page_num_link_search_users page-link")
                        .html("&laquo;")
                )
        );
        for (var i = 0; i < page_numbers.length; i++) {
            if (page_numbers[i] !== null) {
                nr_of_pages_search_users = page_numbers[i];
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
                                        .addClass("btn btn-secondary page_num_link_search_users page-link")
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
                                    .addClass("btn btn-secondary page_num_link_search_users page-link")
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
                        .attr("id", "next-search-users")
                        .addClass("btn btn-secondary page_num_link_search_users page-link")
                        .html("&raquo;")
                )
        );
        $('.page-link').parent().removeClass("active");

        if ($('#basic-search-container').hasClass('d-none')) {
            $('#' + $('#advanced_page_number').val() + '.page-link').parent().addClass("active");
        } else {
            $('#' + $('#basic_page_number').val() + '.page-link').parent().addClass("active");
        }
    }

    function create_table(data) {
        let index_start = 1;
        let per_page = 15;
        if ($('#basic-search-container').hasClass('d-none')) {
            index_start = per_page * (parseInt($('#advanced_page_number').val()) - 1);
        } else {
            index_start = per_page * (parseInt($('#basic_page_number').val()) - 1);
        }
        for (key in data['data']) {
            index_start += 1;
            write_row(data['data'][key], index_start, key);

        }
        if (index_start === 0) {
            $('#empty-results-search-users').css("visibility", "visible");
            $('#paginationBox-search-users').css("visibility", "hidden");
        } else {
            $('#empty-results-search-users').css("visibility", "hidden");
            $('#paginationBox-search-users').css("visibility", "visible");
        }

        $('#paginationBox-search-users').empty();
        if (index_start !== 0) {
            show_page_numbers(data['pages_lst']);
            if ($('#advanced-search-container').hasClass('d-none')) {
                let page = $('#basic_page_number').val();
                $('#advanced-search-form').trigger('reset');
                $('#basic-search-form').trigger('reset');
                $('#basic_page_number').val(page);
            } else {
                let page = $('#advanced_page_number').val();
                $('#advanced-search-form').trigger('reset');
                $('#basic-search-form').trigger('reset');
                $('#advanced_page_number').val(page);
            }

        }
        if ($('#collapse-table-search-users').css("display") === "none") {
            $('#collapse-table-search-users').slideToggle(0);
        } else {
            $('#collapse-table-search-users')
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
                url: "/admin_dashboard_basic_search_users/",
                data: data_form,
                success: function (data) {

                    // $('#basic-search-form').trigger('reset');
                    $('#content-table-search-users').empty();
                    if (data['data'].hasOwnProperty("basic_search_name")) {

                        if ($('#basic_search_name.form-control').hasClass('has-error') === false) {
                            $('#basic_search_name.form-control').addClass('has-error');
                        }

                        $('#basic_search_name_error')
                            .text(data['data']['basic_search_name']['0'])
                            .css("visibility", "visible");

                        if ($('#collapse-table-search-users').css("display") !== "none") {
                            $('#collapse-table-search-users').slideToggle(0);
                        }
                    } else {
                        create_table(data);
                    }
                }

            });
        } else {
            data_form = data_form.replace(/&advanced_page_number=\d+&/, "&advanced_page_number=" + $('#advanced_page_number').val() + "&");
            $.ajax({
                type: "POST",
                url: "/admin_dashboard_advanced_search_users/",
                data: data_form,
                success: function (data) {
                    $('#content-table-search-users').empty();

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

                        if ($('#collapse-table-search-users').css("display") !== "none") {
                            $('#collapse-table-search-users').slideToggle(0);
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
        $('#advanced_page_number').val(1);
        data_form = $('#advanced-search-form').serialize();
        get_data();
        e.preventDefault();
    });

    $('#empty-results-search-users').css("display", "hidden");
    if ($('#content-table-search-users').children().length === 0) {
        $('#empty-results-search-users').css("visibility", "visible");
        $('#paginationBox-search-users').css("visibility", "hidden");
    }
    $(document).on("click", ".page_num_link_search_users", function () {

        let page_nr = 0;
        if ($('#basic-search-container').hasClass('d-none')) {
            page_nr = $('#advanced_page_number');
        } else {
            page_nr = $('#basic_page_number');
        }

        if ($(this).attr("id") === "prev-search-users") {
            if (parseInt(page_nr.val()) <= 1) {
                $(this).trigger("blur");
                return;
            }

            page_nr.val(parseInt(page_nr.val()) - 1);
        } else if ($(this).attr("id") === "next-search-users") {
            if (parseInt(page_nr.val()) >= nr_of_pages_search_users) {
                $(this).trigger("blur");
                return;
            }

            page_nr.val(parseInt(page_nr.val()) + 1);
        } else {
            page_nr.val(parseInt($(this).attr("id")));
        }
        get_data();
    });

    $('#basic_search_name').val("all");
    $('#basic-search-button').trigger('click');

    $(document).on("click", '.edit-search-users-button', function () {

        $('#update-user-modal').modal('show');
        let row_id = $(this).attr("id");
        $('#update_user_id').val(
            $('#user-id-row-content-search-users-'+row_id).text()
        );
        $('#update_user_first_name').val(
            $('#user-first-name-row-content-search-users-'+row_id).text()
        );
        $('#update_user_last_name').val(
           $('#user-last-name-row-content-search-users-'+row_id).text()
        );
        $('#update_user_library_card_id').val(
             $('#user-library-card-id-row-content-search-users-'+row_id).text()
        );
        $('#update_user_book_return_coeff').val(
            $('#user-trust-coeff-row-content-search-users-'+row_id).text()
        );
        $('#update_user_email').val(
             $('#user-email-row-content-search-users-'+row_id).text()
        );
        $('#update_user_type').val(
             $('#user-type-row-content-search-users-'+row_id).text()
        );
        $('#update_user_address').val(
            $('#user-address-row-content-search-users-'+row_id).text()
        );
        $('#update_user_zip_code').val(
            $('#user-zip-code-row-content-search-users-'+row_id).text()
        );
        $('#update_user_city').val(
            $('#user-city-row-content-search-users-'+row_id).text()
        );
        $('#update_user_country').val(
            $('#user-country-row-content-search-users-'+row_id).text()
        );
    });

});