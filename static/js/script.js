$(document).ready(function () {
    let chart;
    const ctx = document.getElementById("chart").getContext("2d");

    // UI Initialization
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.carousel').carousel();
    createGraph();

    // Create Graph
    function createGraph(){
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Open', 'In Progress', 'Resolved', 'On Hold'],
                datasets: [{
                    label: 'Tickets',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)'

                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

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