$('.accordion-toggle').click(function () {

    // if ($('.accordion-toggle').attr('aria-expanded') === "true") {
    //     $('.accordion-toggle').attr('aria-expanded', "false");
    // }
    // if ($('.accordion-toggle').hasClass('collapsed') === "false") {
    //     $('.accordion-toggle').addClass('collapsed');
    // }
    // if ($('.sub-table-row').hasClass("show")) {
    //     $('.sub-table-row').removeClass("show");
    // }
    //
    // $('.hiddenRow').hide();

    $(this).next('tr').find('.hiddenRow').show();
});