$(document).ready(function () {
    $('#email').addClass('form-control');
    $('#password').addClass('form-control');

    $('form').submit(function (e) {
        $('#email-err').css("visibility", "hidden");
        $('#password-err').css("visibility", "hidden");
        $('#invalid-credentials').css("visibility", "hidden");
        if ($('#email').hasClass('has-error')) {
            $('#email').toggleClass('has-error');
        }
        if ($('#password').hasClass('has-error')) {
            $('#password').toggleClass('has-error');
        }

        $.ajax({
            type: "POST",
            url: "/process_login_form",
            data: $('form').serialize(),
            success: function (data) {
                if (data['data'].hasOwnProperty("status") && data['data']['status'] === 200) {
                    window.location = "/account";
                } else if (data['data'] === 'invalid-credentials') {

                    if ($('#email').hasClass('has-error') === false) {
                        $('#email').addClass('has-error');
                    }
                    if ($('#password').hasClass('has-error') === false) {
                        $('#password').addClass('has-error');
                    }
                    $('#invalid-credentials')
                        .text('Invalid username or password !')
                        .css("visibility", "visible");
                } else {
                    for (key in data['data']) {
                        if ($('#' + key).hasClass('has-error') === false) {
                            $('#' + key).addClass('has-error');
                        }
                        $('#' + key + '-err')
                            .text(data['data'][key][0])
                            .css("visibility", "visible");
                    }
                }
            }
        });
        e.preventDefault();
    });
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});
