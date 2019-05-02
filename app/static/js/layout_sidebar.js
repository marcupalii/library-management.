$(document).ready(function () {
    $(window).resize(function () {
        if ($('#button-sidebar').attr("aria-expanded") === "false" && $(window).width() <= 1050){
            $('.content')
                .css("z-index", "-1")
                .delay(1000)
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
            $('.row-offcanvas-left').toggleClass('active');
            $('.content')
                .delay(1000)
                .queue(function (next) {
                    $(this).css("z-index", "1");
                    next();
                });
        } else {
            $('.row-offcanvas-left').toggleClass('active');
            $('.content').css("z-index", "-1");
        }


    });


});

