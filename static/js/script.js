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
  $('.fixed-action-btn').floatingActionButton({
    direction: 'left'
  });
  $("#due_date").datepicker({
    format: 'dd/mm/yyyy',
    minDate: date,
    showClearBtn: true,
    i18n: {
        done: "Select"
    }
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

  $(function() {
    $('.datepicker').keypress(function(event) {
         event.preventDefault();
        return false;
    });
  });

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
          required: true
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
          required: true
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
        required: true
      },
      description: {
          required: true
      },
      attachment: {
          accept: "image/*"
      },
    },
    messages: {
      attachment: {
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
    }
  });
});
