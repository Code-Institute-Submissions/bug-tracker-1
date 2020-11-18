$(document).ready(function () {
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.carousel').carousel();

    // Confirm Password validation.
    $("#password").on("focusout", function (e) {
        if ($(this).val() != $("#confirm-password").val()) {
            $("#confirm-password").removeClass("valid").addClass("invalid");
        } else {
            $("#confirm-password").removeClass("invalid").addClass("valid");
        }
    });
    
    $("#confirm-password").on("input", function (e) {
        if ($("#password").val() != $(this).val()) {
            $(this).removeClass("valid").addClass("invalid");
        } else {
            $(this).removeClass("invalid").addClass("valid");
        }
    });

    // Confirm Email validation.
    $("#email").on("focusout", function (e) {
        if ($(this).val() != $("#confirm-email").val()) {
            $("#confirm-email").removeClass("valid").addClass("invalid");
        } else {
            $("#confirm-email").removeClass("invalid").addClass("valid");
        }
    });
    
    $("#confirm-email").on("keyup", function (e) {
        if ($("#email").val() != $(this).val()) {
            $(this).removeClass("valid").addClass("invalid");
        } else {
            $(this).removeClass("invalid").addClass("valid");
        }
    });
  });