$(document).ready(function () {
    $('[data-toggle="offcanvas"]').click(function () {

        let navar_button = $('#navbar-button');

        if (navar_button.attr('aria-expanded') === "true") {
            navar_button.toggleClass("collapsed");
            $('#ReverseNavbar').toggleClass("show");
        }
        $('.row-offcanvas-left').toggleClass('active');
    });

});

