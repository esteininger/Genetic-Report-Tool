//GLOBAL VARS:
var FOR_WHO_PARA = getParameterByName('for');
var TAG_FILTERS = ['beneficial', 'noteworthy', 'acmg'];
var CURRENT_URL = window.location.href;

// Btn nav collapse
$('#nav .nav-collapse').on('click', function() {
  $('#nav').toggleClass('open');
});

toastr.options = {
  "closeButton": true,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

  $.fn.extend({
    rotaterator: function(options) {

      var defaults = {
        fadeSpeed: 500,
        pauseSpeed: 100,
        child: null
      };

      var options = $.extend(defaults, options);

      return this.each(function() {
        var o = options;
        var obj = $(this);
        var items = $(obj.children(), obj);
        items.each(function() {
          $(this).hide();
        })
        if (!o.child) {
          var next = $(obj).children(':first');
        } else {
          var next = o.child;
        }
        $(next).fadeIn(o.fadeSpeed, function() {
          $(next).delay(o.pauseSpeed).fadeOut(o.fadeSpeed, function() {
            var next = $(this).next();
            if (next.length == 0) {
              next = $(obj).children(':first');
            }
            $(obj).rotaterator({
              child: next,
              fadeSpeed: o.fadeSpeed,
              pauseSpeed: o.pauseSpeed
            });
          })
        });
      });
    }
  });

function updateNav() {
  var elem = $('#nav-report-cta')

  if (getCookie('report_id')) {
    elem.attr("href", `/report/${getCookie('report_id')}`)
    elem.text('My Report')
  }

  if (FOR_WHO_PARA){
    elem.attr("href", `/`)
    elem.text('Integrate Today')
    eraseCookie('report_id');
  }


  // // Create a new XMLHttpRequest.
  // var request = new XMLHttpRequest();
  //
  // // Handle state changes for the request.
  // request.onreadystatechange = function(response) {
  //   if (request.readyState === 4) {
  //     if (request.status === 200) {
  //       // Parse the JSON
  //       var jsonOptions = JSON.parse(request.responseText);
  //
  //       // Loop over the JSON array.
  //       jsonOptions.forEach(function(item) {
  //         // Create a new <option> element.
  //         var option = document.createElement('option');
  //         // Set the value using the item in the JSON array.
  //         option.value = item;
  //         // Add the <option> element to the <datalist>.
  //         dataList.appendChild(option);
  //       });
  //
  //       // Update the placeholder text.
  //       input.placeholder = "e.g. datalist";
  //     } else {
  //       // An error occured :(
  //       input.placeholder = "Couldn't load datalist options :(";
  //     }
  //   }
  // };
  //
  // // Update the placeholder text.
  // input.placeholder = "Loading options...";
  //
  // // Set up and make the request.
  // request.open('GET', 'html-elements.json', true);
  // request.send();

  // console.log(REPORT_ID, REPORT_IS_VALID)


  //does url parameter for_who exist?
  // if (getCookie('report_id')) {
  //   elem.attr("href", `/report/${getCookie('report_id')}`)
  //   elem.text('My Report')
  // }

  // if (FOR_WHO_PARA) {
  //   elem.attr("href", `/`)
  //   elem.text('Integrate Today')
  // } else if (REPORT_IS_VALID == 'True') {
  //   //report exists in session, change URL to report ID
  //   elem.attr("href", `/report/${REPORT_ID}`)
  //   elem.text('My Report')
  //   setCookie('report_id', REPORT_ID, 2)
  // }
}

// window.onload = function() {
  updateNav();
// }
