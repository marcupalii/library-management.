$(function () {
    $('#file-picker').on('change', function () {
        let count = $(this).val().split('\\').length;
        $(this).next('.custom-file-label').html($(this).val().split('\\')[count-1]);
    })

});