$(document).ready(function () {
    $('[data-toggle="collapse"]').click(function () {

        let sidebar = $('.row-offcanvas-left');
        if (sidebar.attr("class") === "order-1 row-offcanvas-left active") {
            sidebar.toggleClass('active');
            $('.content').css('background-color', 'rgba(0, 0, 0, 0)');
        }

    });
});

