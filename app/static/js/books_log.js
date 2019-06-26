$(document).ready(function () {
    var actual_page = $(location).attr('href').match(/page\/([0-9]+)/)[1];
    $('.page-link').parent().removeClass("active");
    $('#' + actual_page + '.page_num_link').parent().addClass("active");

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
        if (parseInt(page) > parseInt($('#nr_of_pages').text())){
            page = $('#nr_of_pages').text();
        }

        let focus = $(location).attr('href').match(/focus[a-zA-Z0-9%=]+/);
        window.location = "/books_log/page/" + page + "/" + focus[0];
    });


    $('#empty-books-log').css("visibility","hidden");
    if ($('#content-table').children().length === 0){
        $('#empty-books-log').css("visibility","visible");
        $('#paginationBox').css("visibility","hidden");
    }

});