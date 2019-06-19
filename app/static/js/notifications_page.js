$(function () {
    $('.modal-button-edit-notification').on("click", function () {
        let nr_row = $(this).attr("id");
        $('#edit-notifications-modal').modal('show');
        $('#content-edit-notification-modal').text(
            $('#content-row-content-' + nr_row).text()
        );
        $('#id-notification').text(
            $('#id-notification-row-content-'+nr_row).text()
        );
        $('#row-index').text(
            $('#nr-row-content-'+nr_row).text()
        );
        console.log( $('#row-index').text());
    });

    $(document).on('click', '#delete-notification-button', function (e) {
        $.ajax({
            type: "DELETE",
            url: "/delete_notification/" +  $('#id-notification').text() + "/",
            success: function (data) {
                console.log(data);
                $('#edit-notifications-modal').modal('hide');
                let index = $('#row-index').text();
                let per_page = 15;

                if (parseInt(index) !== 1 && parseInt(index) % per_page === 1 ){
                    let actual_page = parseInt($(location).attr('href').match(/\/page\/([0-9]+)/)[1].trim());
                    let focus = $(location).attr('href').match(/\/focus%3D([0-9]+)/)[0].trim();
                    console.log('/notifications/page/'+ (actual_page -1).toString() + focus);
                    window.location = '/notifications/page/'+ (actual_page -1).toString() + focus;
                }else{
                    console.log($(location).attr('href'));
                    window.location = $(location).attr('href');
                }
            }
        });
    });

});
