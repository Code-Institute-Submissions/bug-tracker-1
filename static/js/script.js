$(document).ready(function () {

    // UI Initialization
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.carousel').carousel();

  // Toast Fade out
  $(function() {
    $('.toast').delay(500).fadeIn('normal', function() {
      $(this).delay(2500).fadeOut();
    });
  });
});

