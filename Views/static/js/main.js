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
  //does url parameter for_who exist?
  if (getCookie('report_id')) {
    elem.attr("href", `/report/${getCookie('report_id')}`)
    elem.text('My Report')
  }

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

window.onload = function() {
  updateNav();
}
