$(document).ready(function () {

    let actual_page = $(location).attr('href').match(/page\/([0-9]+)/)[1];
    $('.page-link').parent().removeClass("active");
    $('#' + actual_page + '.page_num_link').parent().addClass("active");

    if ($(location).attr('href').match(/focus=0/)) {
    } else {
        let matched = $(location).attr('href').match(/focus%3D([0-9]+)/);
        let rank_id_focus = matched[1].trim();
        $.each($('.rank'), function () {

            if ($(this).text().trim() === rank_id_focus) {
                $(this).parent()
                    .attr("tabindex", -1)
                    .focus();
            }
        });

    }
    $('.page_num_link').click(function () {
        let page = "1";
        if ($(this).attr("id").trim() === "prev") {
            if (parseInt(actual_page) > 1) {
                page = (parseInt(actual_page) - 1).toString()
            }
        } else if ($(this).attr("id").trim() === "next") {
            page = (parseInt(actual_page) + 1).toString()
        } else {
            page = $(this).attr("id").trim();
        }
        if (parseInt(page) > parseInt($('#nr_of_pages').text())) {
            page = $('#nr_of_pages').text();
        }
        let focus = $(location).attr('href').match(/focus[a-zA-Z0-9%=]+/);
        window.location = "/wishlist/page/" + page + "/" + focus[0];
    });
    $('.delete-from-wishlist').click(function () {
        window.location = $(this).attr("id");
    });

    $('#empty-wishlist').css("visibility", "hidden");
    if ($('#content-table').children().length === 0) {
        $('#empty-wishlist').css("visibility", "visible");
        $('#paginationBox').css("visibility", "hidden");
    }
    $('#open-next-book-modal').on("click", function () {
        $('#next-book-deny-button').removeClass("d-none");
        $('#next-book-save-button').removeClass("d-none");
        $('#next_book_id').val($('#next-book-id').text());
        $('#modal-book-name').text($('#book-name-next-book').text());
        $('#modal-book-type').text($('#book-type-next-book').text());
        $('#modal-book-author-first-name').text($('#author-first-name-next-book').text());
        $('#modal-book-author-last-name').text($('#author-last-name-next-book').text());
        $('#modal-book-period-start').text($('#period-start-next-book').text());
        $('#modal-book-period-end').text($('#period-end-next-book').text());

        $('#next-book-modal').modal('show');
    });
    $('#close-next-book-modal').on("click", function () {
        $('#next-book-modal').modal('hide');
    });

    $('#close-next-book-modal').on("click", function () {
        window.location = "/wishlist/page/1/focus=0/";
    });
    $('#next-book-deny-button').on("click", function () {
        $(this).addClass("d-none");
        $('#next-book-save-button').addClass("d-none");
        $.ajax({
            type: "POST",
            url: "/deny_next_book/",
            data: $('#accept-next-book-form').serialize(),
            success: function (data) {

                $('#succes-alert-content').parent().removeClass("d-none");
                $('#succes-alert-content').text("You have successfully deny the new book !");

            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#fail-alert-content').parent().removeClass("d-none");
                $('#fail-alert-content').text("The book is no longer available !")


            }
        });
    });
    $('#next-book-save-button').on("click", function () {
        $(this).addClass("d-none");
        $('#next-book-deny-button').addClass("d-none");
        $.ajax({
            type: "POST",
            url: "/accept_next_book/",
            data: $('#accept-next-book-form').serialize(),
            success: function (data) {
                $('#succes-alert-content').parent().removeClass("d-none");
                $('#succes-alert-content').text("You have successfully accepted the new book !");

            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#fail-alert-content').parent().removeClass("d-none");
                $('#fail-alert-content').text("The book is no longer available !");

            }
        });
    });

    $(document).on('click', '.edit-wishlist-book-button', function (e) {
        e.preventDefault();
        let id_row = $(this).attr("id");
        $('#update-wishlist-rank-modal').modal('show');
        $('#update_wishlist_entry_id').val(
            $('#entry-wishlist-id-nr-row-content-' + id_row).text()
        );

        $('#book-name-update-rank').text(
            $('#book-name-row-content-' + id_row).text()
        );

        $('#book-type-update-rank').text(
            $('#book-type-row-content-' + id_row).text()
        );
        $('#author-first-name-update-rank').text(
            $('#author-first-name-row-content-' + id_row).text()
        );
        $('#author-last-name-update-rank').text(
            $('#author-last-name-row-content-' + id_row).text()
        );
        $('#update_wishlist_rank').val(
            $('#nr-row-content-' + id_row).text().trim()
        );
        $('#update_wishlist_period').val(
            $('#period-row-content-' + id_row).text().trim()
        );


    });

    $('#update-wishlist-rank-button').on("click", function () {
        $.ajax({
            type: "POST",
            url: "/update_wishlist_book/",
            data: $('#update-wishlist-rank-form').serialize(),
            success: function (data) {

                if (!data['data'].hasOwnProperty("id")) {
                    for (let key in data['data']) {
                        for (key in data['data']) {
                            $('#' + key + '_update_rank_error')
                                .css("visibility", "visible")
                                .text(data['data'][key]);
                            $('#' + key).addClass("has-error");
                        }
                    }
                } else {
                    $('#update-wishlist-rank-modal').modal('hide');
                    window.location = $(location).attr('href')
                }
            }
            , error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                window.location = $(location).attr('href')
            }
        });
    });
    $('#delete-wishlist-book-button').on("click", function () {
        $.ajax({
            type: "DELETE",
            url: "/wishlist_delete_entry/" + $('#update_wishlist_entry_id').val() + "/",
            success: function (data) {

                $('#update-wishlist-rank-modal').modal('hide');
                window.location = data['data']['url'];
            }
            , error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                $('#update-wishlist-rank-modal').modal('hide');
                window.location = "/wishlist/page/1/focus=0/";
            }
        });

    });
});