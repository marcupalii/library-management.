$(document).ready(function () {
    $(window).resize(function () {
        if ($('#button-sidebar').attr("aria-expanded") === "false" && $(window).width() <= 1050) {
            $('.content')
                .css("z-index", "-1")
                .delay(1500)
                .queue(function (next) {
                    $(this).css("z-index", "1");
                    next();
                });
        }
    });
    $('[data-toggle="offcanvas"]').click(function () {

        let navar_button = $('#navbar-button');

        if (navar_button.attr('aria-expanded') === "true") {
            navar_button.toggleClass("collapsed");
            $('#ReverseNavbar').toggleClass("show");
        }

        if ($('.row-offcanvas-left').hasClass("active")) {
            $('.row-offcanvas-left').removeClass('active');

            function change_content_index() {
                if ($('.row-offcanvas-left').hasClass("active") === false) {
                    $('.content').css("z-index", "1");
                }
            }

            setTimeout(change_content_index, 1500);

        } else {
            $('.content').css("z-index", "-1");
            $('.row-offcanvas-left').addClass('active');

        }


    });


});

