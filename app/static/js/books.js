$(document).ready(function () {

    $('#type_author-0').next().css("margin-bottom", "0");
    $('#type_author-1').next().css("margin-bottom", "0");

    $('.err-msg').each(function () {
        $(this).css("visibility", "hidden");
    });

    $('#choose-author-container').css("visibility","hidden");
    $('#type_author-0').on("click", function () {
        if ($('#type_author-0').is(':checked')){
             $('#choose-author-container').css("visibility","hidden");
        }else{
             $('#choose-author-container').css("visibility","visible");
        }
    });


    $('#add-new-book-button').on("click", function (e) {
        e.preventDefault();
        $('.err-msg').each(function () {
            $(this).css("visibility", "hidden");
        });

        $.ajax({
            type: "POST",
            url: "/add_new_book/",
            data: $('#new-book-form').serialize(),
            success: function (data) {
                console.log(data['data']);
                if (data['data'].hasOwnProperty("id") === false) {
                    for (key in data['data']) {
                        $('#' + key + '_new_book_error')
                            .css("visibility", "visible")
                            .text(data['data'][key]);

                    }
                } else {
                    $('.err-msg').each(function () {
                        $(this).css("visibility", "hidden");
                    });
                    $('#new-book-form').trigger("reset");
                }
            }
        });
    });
});