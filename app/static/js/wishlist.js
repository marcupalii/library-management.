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
        $('#next_book_id').val($('#next-book-id').text());
        $('#modal-book-name').text($('#book-name-next-book').text());
        $('#modal-book-type').text($('#book-type-next-book').text());
        $('#modal-book-author').text($('#author-next-book').text());
        $('#modal-book-period-start').text($('#period-start-next-book').text());
        $('#modal-book-period-end').text($('#period-end-next-book').text());

        $('#next-book-modal').modal('show');
    });
    $('#close-next-book-modal').on("click", function () {
        $('#next-book-modal').modal('hide');
    });
    $('#next-book-save-button').on("click", function () {
        $.ajax({
            type: "POST",
            url: "/accept_next_book/",
            data:  $('#accept-next-book-form').serialize(),
            success: function (data) {
                console.log(data);
                $('#next-book-modal').modal('hide');
                window.location = "/wishlist/page/1/focus=0/";
            }
        });
    });
});