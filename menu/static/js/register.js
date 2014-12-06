var registerFormFn = function() {
    if ($('input[name="password"]').val() === $('input[name="password2"]').val()) {
        $('form').submit();
    } else {
        $('.register-msg').html('Password compare failed.').show();
    }
};

$(document).ready(function() {

});
