$(document).ready(function () {
    $('[data-toggle="offcanvas"]').click(function () {

        let navar_button = $('#navbar-button');

        if (navar_button.attr('aria-expanded') === "true") {
            navar_button.toggleClass("collapsed");
            $('#ReverseNavbar').toggleClass("show");
        }

        if ($('.row-offcanvas-left').hasClass("active")) {
            $('.row-offcanvas-left').toggleClass('active');
            $('.content')
                .delay(500)
                .queue(function (next) {
                    $(this).css("z-index", "1");
                    next();
                });
        } else {
            $('.row-offcanvas-left').toggleClass('active');
            $('.content')
                .delay(500)
                .queue(function (next) {
                    $(this).css("z-index", "-1");
                    next();
                });
        }


    });


});

