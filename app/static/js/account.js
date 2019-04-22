$(function () {

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


    $('#option-0').prop('checked', true);

    function get_autocomplete(option) {
        $.ajax({
            url: "/autocomplete/" + option + "/",
            type: 'GET',
            contentType: 'application/json;charset=UTF-8',
        }).done(function (data) {
            console.log(data);
            $('#name_autocomplete').autocomplete({
                minLength: 1,
                source: function (req, resp) {
                    var match = new RegExp("^" + $.ui.autocomplete.escapeRegex(req.term), "i");
                    resp($.grep(data, function (el) {
                        return match.test(el);
                    }));
                }
            });
        });
    }

    get_autocomplete("1");

    $(document).on('change', 'input:radio[id^="option-"]', function () {
        get_autocomplete($(this)[0].value);
    });


    $('form').submit(function (e) {
        $('#name-err').css("visibility", "hidden");
        if ($('#name_autocomplete').hasClass('has-error')) {
            $('#name_autocomplete').toggleClass('has-error');
        }

        $.ajax({
            type: "POST",
            url: "/process_search_form/",
            data: $('form').serialize(),
            success: function (data) {
                var error = "true";

                $('#name_autocomplete').val('');
                $('#content-table').empty();
                var i = 0;
                for (key in data['data']) {
                    if (key === "autocomp") {
                        if ($('#name_autocomplete').hasClass('has-error') === false) {
                            $('#name_autocomplete').addClass('has-error');
                        }
                        $('#name-err').text(data['data'][key][0]);
                        $('#name-err').css("visibility", "visible");

                        break;

                    } else {
                        if (error === "true") {
                            error = "false";
                        }
                        i += 1;
                        $('#content-table')
                            .append(
                                $('<tr/>')
                                    .attr("colspan", "6")
                                    .append(
                                        $('<td/>')
                                            .text(i.toString())
                                            .attr("id", "nr-row-content-" + i.toString())
                                    )
                                    .append(
                                        $('<td/>')
                                            .text(data['data'][key]['book_name'])
                                            .attr("id", "book-name-row-content-" + i.toString())
                                    )
                                    .append(
                                        $('<td/>')
                                            .text(data['data'][key]['book_type'])
                                            .attr("id", "book-type-row-content-" + i.toString())
                                    )
                                    .append(
                                        $('<td/>')
                                            .text(data['data'][key]['author_name'])
                                            .attr("id", "author-name-row-content-" + i.toString())
                                            .addClass("d-none d-md-block")
                                    )

                                    .append(
                                        $('<td/>')
                                            .text(data['data'][key]['count_book'])
                                            .addClass("d-none d-lg-block")
                                            .attr("id", "count-book-row-content-" + i.toString())
                                    )
                                    .append(
                                        $('<td/>')
                                            .append(
                                                $('<button/>')
                                                    .addClass("btn accordion-toggle d-lg-none")
                                                    .attr("data-toggle", "collapse")
                                                    .attr("data-target", "#tr-collapse-id-" + i.toString())
                                                    .attr("aria-controls", "aria-controls" + i.toString())
                                                    .attr("id", i.toString())
                                                    .attr("type", "button")
                                                    .append(
                                                        $('<i/>')
                                                            .addClass("fas fa-expand-arrows-alt")
                                                    )
                                            )
                                            .append(
                                                $('<button/>')
                                                    .addClass("btn modal-button")
                                                    .attr("id", i.toString())
                                                    .attr("type", "button")
                                                    .append(
                                                        $('<i/>')
                                                            .addClass("fas fa-external-link-alt")
                                                    )
                                            )
                                    )
                            );


                        $('#content-table').append(
                            $('<tr/>')
                                .addClass("sub-table-row p collapse p-3 tr-collapse-" + i.toString())
                                .attr("id", "tr-collapse-id-" + i.toString())
                                .append(
                                    $('<td/>')
                                        .attr("colspan", "6")
                                        .addClass("hiddenRow")
                                        .append(
                                            $('<div/>')
                                                .addClass("accordian-body")
                                                .append(
                                                    $('<p/>')
                                                        .addClass("d-md-none")
                                                        .text("author_name: ")
                                                        .append(
                                                            $('<span/>')
                                                                .text(data['data'][key]['author_name'])
                                                        )
                                                )
                                                .append(
                                                    $('<p/>')
                                                        .addClass("d-lg-none")
                                                        .text("Status : ")
                                                        .append(
                                                            $('<span/>')
                                                                .text(data['data'][key]['count_book'])
                                                        )
                                                )
                                        )
                                )
                        );
                    }
                }

                if (i === 0) {
                    error = "false";
                    $('#content-table').css("text-align", "center").text("no results find !");
                }
                if (error === "false") {
                    if ($('#collapse-table').css("display") === "none") {

                        $('#collapse-table').slideToggle(500);
                    } else {
                        $('#collapse-table').slideToggle(0);
                        $('#collapse-table').slideToggle(500);
                    }
                } else {
                    if ($('#collapse-table').css("display") !== "none") {
                        $('#collapse-table').slideToggle(0);
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
    });


    $.extend($.ui.autocomplete.prototype.options, {

        open: function (event, ui) {

            if ($('#name_autocomplete').val() !== "") {
                $('#name-err').css("visibility", "hidden");
                if ($('#name_autocomplete').hasClass('has-error')) {
                    $('#name_autocomplete').toggleClass('has-error');
                }
            }


            $(".selector").autocomplete({autoFocus: true});
            $(this).autocomplete("widget").css({
                "width": ($('#search-container').width() + "px")
            });

            $('.ui-menu-item').css("width", "99%");

            $('.ui-menu-item').css("margin-left", "1.5px");

        }
        ,
    })
    ;

    $(window).resize(function () {
        $(".ui-menu").css({"display": "none"});
    });

});


$(document).on("click", ".modal-button", function () {
    let id = $(this).attr("id");
    console.log(id);
    $('#no').text($("#nr-row-content-" + id).text());
    $('#book-name').text($("#book-name-row-content-" + id).text());
    $('#book-type').text($("#book-type-row-content-" + id).text());
    $('#author-name').text($("#author-name-row-content-" + id).text());
    $('#status').text($("#count-book-row-content-" + id).text());

    $('#myModal').modal('toggle');
});