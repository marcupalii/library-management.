$(document).ready(function () {

    let page = $(location).attr('href').match(/page\/([0-9])+/)[1];
    $('.page-link').parent().removeClass("active");
    $('#'+page+'.page_num_link').parent().addClass("active");

    if ($(location).attr('href').match(/focus=0/)) {
    } else {
        let matched = $(location).attr('href').match(/focus%3D([0-9]+)/);
        let rank_id_focus = matched[1].trim();
        $.each($('.rank'), function () {

            if ($(this).text().trim() === rank_id_focus) {
                // $('html, body').animate({ scrollTop: $(this).parent().offset().top }, 'slow');
                // $(this).parent().focus();

                $(this).parent()
                    .attr("tabindex", -1)
                    .focus();

                // $(this)
                //     .parent()
                //     .css('outline', 'none !important')
                //     .attr("tabindex", -1)
                //     .focus();
            }
        });

    }
    $('.page_num_link').click(function () {
        let page = $(this).attr("id").trim();
        let focus = $(location).attr('href').match(/focus[a-zA-Z0-9%=]+/);
        window.location = "/books_log/page/"+page+"/" + focus[0];
    });
});