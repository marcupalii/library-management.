$(document).ready(function () {
    $(window).resize(function () {
        if ($('#button-sidebar').attr("aria-expanded") === "false" && $(window).width() <= 1050 && $(window).width() >= 1010) {
            if ($('.row-offcanvas-left').hasClass("overlay-z-index-above") === false) {
                $('.row-offcanvas-left').addClass("overlay-z-index-above");
            }
            $('.content')
                .addClass("overlay-z-index-under")
                .delay(1500)
                .queue(function (next) {
                    $(this).removeClass("overlay-z-index-under");
                    next();
                });

        }
    });
    var trans = false;
    $('[data-toggle="offcanvas"]').click(function (e) {
        if (!$('.row-offcanvas-left').hasClass("overlay-z-index-above")) {
            $('.row-offcanvas-left').addClass("overlay-z-index-above");
        }

        if (trans === false) {
            console.log(trans);
            trans = true;
        } else {
            e.stopPropagation();
            e.preventDefault();
            return;
        }


        let navar_button = $('#navbar-button');

        if (navar_button.attr('aria-expanded') === "true") {
            navar_button.toggleClass("collapsed");
            $('#ReverseNavbar').toggleClass("show");
        }

        if ($('.row-offcanvas-left').hasClass("active")) {
            $('.row-offcanvas-left').removeClass('active');

            function change_content_index() {

                $('.content').removeClass("overlay-z-index-under");
                $('.row-offcanvas-left').removeClass("overlay-z-index-above");
                trans = false;

            }

            setTimeout(change_content_index, 700);

        } else {
            $('.content').addClass("overlay-z-index-under");
            if (!$('.row-offcanvas-left').hasClass("overlay-z-index-above")) {
                $('.row-offcanvas-left').addClass("overlay-z-index-above");
            }
            $('.row-offcanvas-left').addClass('active');
            trans = false;

        }


    });


});

