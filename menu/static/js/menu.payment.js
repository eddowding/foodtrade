$(document).ready(function() {
  var $form = $('#paymentModal form');
  $('#paymentModal button.payment-add-btn').click(payWithStripe);

  /* If you're using Stripe for payments */
  function payWithStripe(e) {
    console.log(e);
    e.preventDefault();

    /* Visual feedback */
    $('#paymentModal button.payment-add-btn').html('Validating <i class="fa fa-spinner fa-pulse"></i>');

    Stripe.card.createToken($form, function stripeResponseHandler(status, response) {
      console.log(status, response);
      if (response.error) {
        /* Visual feedback */
        $('#paymentModal button.payment-add-btn').html('Try again');
        /* Show Stripe errors on the form */
        $form.find('.payment-errors').text(response.error.message);
        $form.find('.payment-errors').closest('.row').show();
      } else {
        /* Visual feedback */
        $('#paymentModal button.payment-add-btn').html('Processing <i class="fa fa-spinner fa-pulse"></i>');
        /* Hide Stripe errors on the form */
        $form.find('.payment-errors').closest('.row').hide();
        $form.find('.payment-errors').text("");
        // response contains id and card, which contains additional card details
        var token = response.id;
        console.log(token);
        // AJAX
        if ($form.find('[name=couponCode]').val()) {
          response.coupon = $form.find('[name=couponCode]').val();
        }
        $.post(stripeCardTokenUrl, response)
          // Assign handlers immediately after making the request,
          .done(function(data, textStatus, jqXHR) {
            $('#paymentModal button.payment-add-btn').html('Payment successful <i class="fa fa-check"></i>').prop('disabled', true);
            window.location.reload();
          })
          .fail(function(jqXHR, textStatus, errorThrown) {
            $('#paymentModal button.payment-add-btn').html('There was a problem').removeClass('success').addClass('error');
            /* Show Stripe errors on the form */
            $form.find('.payment-errors').text('Try refreshing the page and trying again.');
            $form.find('.payment-errors').closest('.row').show();
          });
      }
    });
  }

  /* Form validation */
  jQuery.validator.addMethod("month", function(value, element) {
    return this.optional(element) || /^(01|02|03|04|05|06|07|08|09|10|11|12)$/.test(value);
  }, "Please specify a valid 2-digit month.");

  jQuery.validator.addMethod("year", function(value, element) {
    return this.optional(element) || /^[0-9]{2}$/.test(value);
  }, "Please specify a valid 2-digit year.");

  validator = $form.validate({
    rules: {
      cardNumber: {
        required: true,
        creditcard: true,
        digits: true
      },
      expMonth: {
        required: true,
        month: true
      },
      expYear: {
        required: true,
        year: true
      },
      cvCode: {
        required: true,
        digits: true
      }
    },
    highlight: function(element) {
      $(element).closest('.form-control').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
      $(element).closest('.form-control').removeClass('error').addClass('success');
    },
    errorPlacement: function(error, element) {
      $(element).closest('.form-group').append(error);
    }
  });

  paymentFormReady = function() {
    if ($form.find('[name=cardNumber]').hasClass("success") &&
      $form.find('[name=expMonth]').hasClass("success") &&
      $form.find('[name=expYear]').hasClass("success") &&
      $form.find('[name=cvCode]').val().length > 1) {
      return true;
    } else {
      return false;
    }
  }

  $('#paymentModal button.payment-add-btn').prop('disabled', true);
  var readyInterval = setInterval(function() {
    if (paymentFormReady()) {
      $('#paymentModal button.payment-add-btn').prop('disabled', false);
      clearInterval(readyInterval);
    }
  }, 250);

  $('.stripe-coupon-btn').click(function() {
    $.ajax({
      url: stripeCouponValueUrl,
      data: {coupon: $form.find('[name=couponCode]').val()},
      success: function(data) {
        if (data.success) {
          $form.find('.payment-errors').closest('.row').hide();
          $('.stripe-price').html(data.amount);
        } else {
          $form.find('.payment-errors').text('Invalid coupon code.');
          $form.find('.payment-errors').closest('.row').show();
          $('.stripe-price').html(stripePlanAmount);
        }
      }
    });
  });
});
