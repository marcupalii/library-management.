$(document).ready(function () {
    $(window).resize(function () {
        if ($('#button-sidebar').attr("aria-expanded") === "false" && $(window).width() <= 1050 && $(window).width() >= 1010 ) {
            $('.content')
                .addClass("overlay-z-index-under")
                .delay(1500)
                .queue(function (next) {
                    $(this).removeClass("overlay-z-index-under");
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
                    $('.content').removeClass("overlay-z-index-under");
                }
            }

            setTimeout(change_content_index, 1500);

        } else {
            $('.content').addClass("overlay-z-index-under");
            $('.row-offcanvas-left').addClass('active');

        }


    });


});

