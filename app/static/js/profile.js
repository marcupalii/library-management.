$(function () {

    $('#old_password_error').css('visibility', 'hidden');
    $('#new_password_error').css('visibility', 'hidden');
    $('#retype_password_error').css('visibility', 'hidden');

    $('#update-password-button').click(function () {

        $('#old_password_error').css('visibility', 'hidden');
        $('#new_password_error').css('visibility', 'hidden');
        $('#retype_password_error').css('visibility', 'hidden');

        $('#old_password').removeClass("has-error");
        $('#new_password').removeClass("has-error");
        $('#retype_password').removeClass("has-error");

        $.ajax({
                type: "POST",
                url: "/change_password/",
                data: $('#change-password-form').serialize(),
                success: function (data) {
                    console.log(data['data']);
                    if (data['data'].hasOwnProperty("succes") !== true) {
                        for (key in data['data']) {
                            console.log(key);
                            $('#' + key + '_error')
                                .css("visibility", "visible")
                                .text(data['data'][key]);
                            $('#' + key).addClass("has-error");
                        }
                    } else {
                        $('#change-password-form').trigger('reset');
                    }
                }

            }
        )
    });
});