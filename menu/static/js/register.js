$(document).ready(function() {
    $('input[name="first_name"]').focus();

    $('.form-control').focusout(function(ev) {
        var parentDiv = $(this).parent();
        var helpTextDiv = parentDiv.find('.help-text');
        if (!$(this).val()) {
            parentDiv.addClass('has-error');
            helpTextDiv.html('This is required.');
            $('.signup').addClass('disabled');
        } else {
            parentDiv.removeClass('has-error');
            helpTextDiv.html('');
            $('.signup').removeClass('disabled');
        }
    });

    $('input[name="username"]').focusout(function(ev) {
        var username = $(this).val();
        var parentDiv = $(this).parent();
        var helpTextDiv = parentDiv.find('.help-text');
        $.ajax({
            url: '/menu/user/lookup/count',
            data: {
                username: username
            },
            type: 'GET',
            dataType: 'JSON',
            success: function(data) {
                if (data.count > 0) {
                    parentDiv.addClass('has-error');
                    helpTextDiv.html('Username already exists.');
                    $('.signup').addClass('disabled');
                } else {
                    parentDiv.removeClass('has-error');
                    helpTextDiv.html('');
                    $('.signup').removeClass('disabled');
                }
            }
        });
    });

    $('.signup').click(function() {
        var formHasError = $('.form-group').hasClass('has-error');
        if (($('.form-group').hasClass('has-error') == false) && ($('input[name="password"]').val() === $('input[name="password2"]').val())) {
            $('form').submit();
        }
    });
});
