$(function () {
    $('#file').on('change', function () {
        let count = $(this).val().split('\\').length;
        $(this).next('.custom-file-label').html($(this).val().split('\\')[count - 1]);
    });
    $.each($('.form-control'), function () {
        if ($(this).parent().next('.err-msg').text() !== "") {
            $(this).addClass("has-error");
        }
    });
    if($('#first_name_new_user_error').text()!== ""){
        $('#file').addClass("has-error");
    }
});