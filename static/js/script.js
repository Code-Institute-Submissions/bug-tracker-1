$(document).ready(function () {

  var date = new Date(); 

  // UI Initialization
  $(".dropdown-trigger").dropdown();
  $('.sidenav').sidenav();
  $('.collapsible').collapsible();
  $('.tabs').tabs();
  $('select').formSelect();
  $('.carousel').carousel();
  $('.modal').modal();
  $("#due_date").datepicker({
    format: 'dd/mm/yyyy',
    minDate: date
  });
  $("#dob").datepicker({
    format: 'dd/mm/yyyy',
    yearRange: [1950, 2002],
    showClearBtn: true,
    i18n: {
        done: "Select"
    }
  });

  // Toast Fade out
  $(function() {
    $('.toast').delay(500).fadeIn('normal', function() {
      $(this).delay(2500).fadeOut();
    });
  });

  // Custom date validation method
  $.validator.addMethod("anyDate",
    function(value, element) {
        return value.match(/^(0?[1-9]|[12][0-9]|4[0-1])[/., -](0?[1-9]|1[0-2])[/., -](19|20)?\d{2}$/);
    },
    "Please enter a valid date."
  );

  // Signup Form Validation
  $("#signup_form").validate({
    rules: {
        username: {
          required: true,
        },
        name: {
            required: true,
        },
        dob: {
          required: true,
          anyDate: true
        },
        email: {
            required: true,
            email: true
        },
        password: {
            minlength: 5
        },
        profile_picture: {
            accept: "image/*"
        }
    },
    messages: {
      profile_picture: {
        accept: "Only images are accepted."
      }
    },
    errorElement : 'div',
    errorPlacement: function(error, element) {
      var placement = $(element).data('error');
      if (placement) {
        $(placement).append(error)
      } else {
        error.insertAfter(element);
      }
    },
  });
  
  // Edit Profile Form
  $("#edit_profile_form").validate({
    rules: {
        name: {
            required: true,
        },
        dob: {
          required: true,
          anyDate:true
        },
        email: {
            required: true,
            email:true
        },
        password: {
            minlength: 5
        },
        profile_picture: {
            accept: "image/*"
        }
    },
    messages: {
      profile_picture: {
        accept: "Only images are accepted."
      }
    },
    errorElement : 'div',
    errorPlacement: function(error, element) {
      var placement = $(element).data('error');
      if (placement) {
        $(placement).append(error)
      } else {
        error.insertAfter(element);
      }
    },
  });

  // New Ticket Form
  $("#new_ticket_form").validate({
    rules: {
      title: {
          required: true,
      },
      due_date: {
        required: true,
        anyDate:true
      },
      description: {
          required: true
      },
      attachment: {
          extension: "pdf, jpeg, jpg, png, gif"
      },
    },
    messages: {
      attachment: {
        extension: "Only images or PDF attachments are accepted."
      }
    },
    errorElement : 'div',
    errorPlacement: function(error, element) {
      var placement = $(element).data('error');
      if (placement) {
        $(placement).append(error)
      } else {
        error.insertAfter(element);
      }
    }
  });
});
