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
          maxLength: 15,
          required: true,
        },
        name: {
            maxLength: 40,
            required: true
        },
        dob: {
          required: true
        },
        email: {
            required: true,
            email: true
        },
        password: {
            minlength: 5,
            maxLength: 15
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
          maxLength: 40,
          required: true
        },
        dob: {
          required: true
        },
        email: {
            required: true,
            email:true
        },
        password: {
            minlength: 5,
            maxLength: 15
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
          minlength: 5,
          maxlength: 50,
          required: true
      },
      due_date: {
        required: true
      },
      description: {
          maxLength: 500,
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

  
  function tickets_count(data) {
    var open = [],
        in_progress = [],
        resolved = [],
        on_hold = [], 
        filtered_open = [],
        filtered_in_progress = [],
        filtered_resolved = [],
        filtered_on_hold = []

    // Count Total Tickets
    data[0].forEach(element => {
      if (element.status == "Open") {
        open.push(element);
      }
      if (element.status == "In Progress") {
        in_progress.push(element);
      }
      if (element.status == "Resolved") {
        resolved.push(element);
      }
      if (element.status == "On Hold") {
        on_hold.push(element);
      }
  
    });  

    // Count User Tickets
    data[1].forEach(element => {
      if (element.status == "Open") {
        filtered_open.push(element);
      }
      if (element.status == "In Progress") {
        filtered_in_progress.push(element);
      }
      if (element.status == "Resolved") {
        filtered_resolved.push(element);
      }
      if (element.status == "On Hold") {
        filtered_on_hold.push(element);
      }
  
    }); 
    return[open.length, in_progress.length, resolved.length, on_hold.length, 
      filtered_open.length, filtered_in_progress.length, filtered_resolved.length, filtered_on_hold.length];
  }

  if (window.location.pathname == "/stats"){

    var getData = $.get("/chart");
    getData.done(function(response) {

      tickets_count = tickets_count(response);
      var ctx = document.getElementById("chart_stats").getContext("2d");

        if(chart_stats)
        {chart_stats.destroy();}

      var chart_stats = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Open', 'In Progress', 'Resolved', 'On Hold'],
            datasets: [{
                backgroundColor: [
                  "#757575  ", "#1565c0  ", "#2e7d32 ", "#e65100 " 
                ],
                data: [tickets_count[0], tickets_count[1], tickets_count[2], tickets_count[3]]
            }]
        },
        options: {
          legend: {
            display: false
        }}
      });
      $("#card_open").text(tickets_count[4])
      $("#card_in_progress").text(tickets_count[5])
      $("#card_resovled").text(tickets_count[6])
      $("#card_on_hold").text(tickets_count[7])
    })
  }
});
