$(document).ready(function () {

  var date = new Date();

    // UI Initialization
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('select').formSelect();
    $('.carousel').carousel();
    $("#due_date").datepicker({
      minDate: date
    });
    $("#dob").datepicker({
      yearRange: [1950, 2002]
    });

  // Toast Fade out
  $(function() {
    $('.toast').delay(500).fadeIn('normal', function() {
      $(this).delay(2500).fadeOut();
    });
  });
});

