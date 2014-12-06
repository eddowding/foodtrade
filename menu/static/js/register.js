var registerFormFn = function() {
    if ($('input[name="password"]').val() === $('input[name="password2"]').val()) {
        $('form').submit();
    } else {
        $('.register-msg').html('Password compare failed.').removeClass('hidden');
    }
};

$(document).ready(function() {
    $('input[name="username"]').focusout(function(ev) {
        var username = $(this).val();
        $.ajax({
            url: '/menu/user/lookup/count',
            data: {
                username: username
            },
            type: 'GET',
            dataType: 'JSON',
            success: function(data) {
                if (data.count > 0) {
                    $('.register-msg').html('Username exists.').removeClass('hidden');
                }
            }
        });
    });
});
