$(document).ready(function () {
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

});