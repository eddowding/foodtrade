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
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
     	if (!re.test(username)){
     		parentDiv.addClass('has-error');
            helpTextDiv.html('Enter valid email address.');
            $('.signup').addClass('disabled');
            var wrong_email = true;
     	}
     	else{
     		parentDiv.removeClass('has-error');
            helpTextDiv.html('');
            $('.signup').removeClass('disabled');
            var wrong_email = false;
     	}
        $.ajax({
            url: '/menu/user/lookup/count/',
            data: {
                username: username
            },
            type: 'GET',
            dataType: 'JSON',
            success: function(data) {
                if (data.count > 0) {
                    parentDiv.addClass('has-error');
                    if (wrong_email)
                    	helpTextDiv.html('Enter valid email address.');
                    else
                    	helpTextDiv.html('Username already exists.');
                    $('.signup').addClass('disabled');
                } else {
                    parentDiv.removeClass('has-error');
                    if (wrong_email)
                    	helpTextDiv.html('Enter valid email address.');
                    else
                    	helpTextDiv.html('');
                    $('.signup').removeClass('disabled');
                }
            }
        });
    });

    $('.signup').click(function() {
        var formHasError = $('.form-group').hasClass('has-error');
        var passwordMatch = ($('input[name="password"]').val() === $('input[name="password2"]').val());
        var termAccepted = $('.form-group').find('.checkbox').find('input[name="terms"]').is(':checked');
        if (formHasError === false && passwordMatch === true) {
            if (termAccepted) {
                $('#registration-form').submit();
            } else {
                $('.form-group').find('.checkbox').parent().find('.help-text').html('You need to accept terms');
            }

        } else if (passwordMatch === false) {
            var parentDiv = $('input[name="password2"]').parent();
            var helpTextDiv = parentDiv.find('.help-text');
            parentDiv.addClass('has-error');
            helpTextDiv.html('Password miss match.');
        }
    });
});
