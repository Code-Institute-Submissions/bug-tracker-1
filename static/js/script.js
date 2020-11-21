$(document).ready(function () {

    // UI Initialization
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.carousel').carousel();
    // createGraph();

    // let chart;
    // const ctx = document.getElementById("chart").getContext("2d");

    // // Create Graph
    // function createGraph(){
    //     var chart = new Chart(ctx, {
    //         type: 'bar',
    //         data: {
    //             labels: ['Open', 'In Progress', 'Resolved', 'On Hold'],
    //             datasets: [{
    //                 label: 'Tickets',
    //                 data: [12, 19, 3, 5, 2, 3],
    //                 backgroundColor: [
    //                     'rgba(255, 99, 132, 0.2)',
    //                     'rgba(54, 162, 235, 0.2)',
    //                     'rgba(255, 206, 86, 0.2)',
    //                     'rgba(75, 192, 192, 0.2)'

    //                 ],
    //                 borderColor: [
    //                     'rgba(255, 99, 132, 1)',
    //                     'rgba(54, 162, 235, 1)',
    //                     'rgba(255, 206, 86, 1)',
    //                     'rgba(75, 192, 192, 1)'
    //                 ],
    //                 borderWidth: 1
    //             }]
    //         },
    //         options: {
    //             scales: {
    //                 yAxes: [{
    //                     ticks: {
    //                         beginAtZero: true
    //                     }
    //                 }]
    //             }
    //         }
    //     });
    // }
    $("form[name=signup_form").submit(function(e) {

      var $form = $(this);
      var $error = $form.find(".error");
      var data = $form.serialize();
    
      $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
          window.location.href = "/dashboard/";
        },
        error: function(resp) {
          $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
      });
    
      e.preventDefault();
    });

    $("form[name=login_form").submit(function(e) {

      var $form = $(this);
      var $error = $form.find(".error");
      var data = $form.serialize();
    
      $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
          window.location.href = "/dashboard/";
        },
        error: function(resp) {
          $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
      });
    
      e.preventDefault();
    });
});

