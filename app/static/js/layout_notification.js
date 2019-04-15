$(function () {

    var count = 0;
    var notifications = [];

    appNotifications = {

        init: function () {

            $("#notificationsBadge").hide();
            $("#notificationNone").hide();
            appNotifications.get_Notifications();

            $("#notifications-dropdown").on('click', function () {
                appNotifications.load();
            });


            setInterval(function () {
                appNotifications.get_Notifications();
                var open = $("#notifications-dropdown").attr("aria-expanded");
                if (open === "false") {
                    $('#notificationsContainer').empty();
                }
            }, 30000);


            $('.notification-read-desktop').on('click', function (event) {
                appNotifications.markAsRead(event, $(this));
            });

        },

        badgeLoadingMask: function (show) {
            let not_badge = $('#notificationsBadge');
            let not_icon = $("#notificationsIcon");
            if (show === true) {
                not_badge.html(appNotifications.badgeSpinner);
                not_badge.show();
            } else {
                not_badge.html(count);
                if (count > 0) {
                    not_icon.removeClass("fa-bell-o");
                    not_icon.addClass("fa-bell");
                    not_badge.show();

                } else {
                    not_icon.addClass("fa-bell-o");
                    not_badge.hide();
                }
            }
        },

        loadingMask: function (show) {

            if (show === true) {
                $("#notificationNone").hide();
                $("#notificationsLoader").show();
            } else {
                $("#notificationsLoader").hide();
                if (count > 0) {
                    $("#notificationNone").hide();
                } else {
                    $("#notificationNone").show();
                }
            }

        },


        get_Notifications: function () {
            appNotifications.badgeLoadingMask(true);
            $.ajax({
                url: "/get_notification/",
                type: "GET",
                dataType: "json",
                success: function (data) {
                    count = 0;
                    notifications.length = 0;
                    $.each(data, function (k, item) {
                        notifications.push({
                            date: item.date_,
                            href: item.href_,
                            text: item.text_,
                            id_not: k,
                        });
                        count += 1;
                    });
                }
            });


            setTimeout(function () {
                $("#notificationsBadge").html(count);
                appNotifications.badgeLoadingMask(false);
            }, 1000);
        },


        load: function () {
            appNotifications.loadingMask(true);
            $("#notificationsBadge").html(count);
            $('#notificationsContainer').html("");

            setTimeout(function () {


                for (let i = 0; i < count; i++) {

                    var template = $('#notificationTemplate').html();
                    template = template.replace("{ href }", notifications[i].href);
                    // template = template.replace("{{image}}", notifications[i].image);
                    template = template.replace("{ text }", notifications[i].text);
                    template = template.replace("{ date }", notifications[i].date);
                    template = template.replace("{ notification_id }", notifications[i].id_not);
                    $('#notificationsContainer').append(template);
                }

                $('.notification-read').on('click', function (event) {
                    appNotifications.markAsRead(event, $(this));
                });

                appNotifications.loadingMask(false);


                $("#notifications-dropdown").prop("disabled", false);
            }, 1000);
        },


        markAsRead: function (event, elem) {

            event.preventDefault();
            event.stopPropagation();

            let id = $(elem.parent()).children().last().text();

            elem.parent('.dropdown-notification').removeClass("notification-unread");


            notifications = $(notifications).filter(function (idx) {
                return notifications[idx].id_not !== id;
            });

            $.ajax({
                url: "/mark_notification_read/",
                type: 'POST',
                contentType: 'application/json;charset=UTF-8',
                data: {'id': id}
            });

            if (document.activeElement) {
                document.activeElement.blur();
            }

            count--;

            appNotifications.load();
        },

        badgeSpinner: '<i class="fa fa-spinner fa-pulse fa-fw" aria-hidden="true"></i>'
    };

    appNotifications.init();

});