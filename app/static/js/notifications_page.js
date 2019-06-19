$(function () {
    $('.modal-button-edit-notification').on("click", function (e) {
        e.preventDefault();
        let nr_row = $(this).attr("id");
        $('#edit-notifications-modal').modal('show');
        $('#content-edit-notification-modal').text(
            $('#content-row-content-' + nr_row).text()
        );
        $('#id-notification').text(
            $('#id-notification-row-content-' + nr_row).text()
        );
        $('#row-index').text(
            $('#nr-row-content-' + nr_row).text()
        );
        let status = $('#status-row-content-' + nr_row).text().trim();
        console.log(status);
        if (status === "unread") {
            $.ajax({
                type: "GET",
                url: "/notification_read/" + $('#id-notification').text() + "/",
                success: function (data) {
                }
            });
        }
    });
    $('#close-edit-notifications-modal').on("click", function (e) {
        e.preventDefault();
        $('#edit-notifications-modal').modal('hide');
        window.location = $(location).attr('href');
    });
    $(document).on('click', '#delete-notification-button', function (e) {
        $.ajax({
            type: "DELETE",
            url: "/delete_notification/" + $('#id-notification').text() + "/",
            success: function (data) {
                console.log(data);
                $('#edit-notifications-modal').modal('hide');
                let index = $('#row-index').text();
                if (parseInt(index) !== 1 && $('#content-table').children().length === 2) {
                    let actual_page = parseInt($(location).attr('href').match(/\/page\/([0-9]+)/)[1].trim());
                    let focus = $(location).attr('href').match(/\/focus%3D([0-9]+)/)[0].trim();
                    console.log('/notifications/page/' + (actual_page - 1).toString() + focus);
                    window.location = '/notifications/page/' + (actual_page - 1).toString() + focus;
                } else {
                    console.log($(location).attr('href'));
                    window.location = $(location).attr('href');
                }
            }
        });
    });

});
