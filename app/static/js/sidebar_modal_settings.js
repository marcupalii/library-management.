$(function () {
    $('#sidebar-modal-settings').modal('hide');
    $('.button-all-notifications').click(function () {
       window.location = $(this).attr("id");
    });
});
$(document).on("click", "#settings-button", function () {
    $('#sidebar-modal-settings').modal('show');
});

$(document).on("click", "#close-settings", function () {
    $('#sidebar-modal-settings').modal('hide');
});
$(document).on("click", "#sidebar-save-settings-button", function () {
    $.ajax({
        type: "POST",
        url: "/save_settings/",
        data: $('#sidebar-settings-form').serialize(),
        success: function (data) {
            $('#sidebar-settings-form').trigger('reset');
            $('#sidebar-modal-settings').modal('hide');
            $('#setting_option-'+(parseInt(data['option'][0])-1).toString()).prop('checked',true);
        }
    })

});
