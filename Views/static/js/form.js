console.log('hi')
! function(t) {
  "use strict";
  var i = function() {
    this.$body = t("body"), this.$portletIdentifier = ".portlet", this.$portletCloser = '.portlet a[data-toggle="remove"]', this.$portletRefresher = '.portlet a[data-toggle="reload"]'
  };
  i.prototype.init = function() {
    var i = this;
    t(document).on("click", this.$portletCloser, function(o) {
      o.preventDefault();
      var e = t(this).closest(i.$portletIdentifier),
        n = e.parent();
      e.slideUp("slow", function() {
        t(this).remove()
      }), 0 == n.children().length && n.slideUp("slow", function() {
        t(this).remove()
      })
    }), t(document).on("click", this.$portletRefresher, function(o) {
      o.preventDefault();
      var e = t(this).closest(i.$portletIdentifier);
      e.append('<div class="panel-disabled"><div class="portlet-loader"></div></div>');
      var n = e.find(".panel-disabled");
      setTimeout(function() {
        n.fadeOut("fast", function() {
          n.remove()
        })
      }, 500 + 300 * (5 * Math.random()))
    })
  }, t.Portlet = new i, t.Portlet.Constructor = i
}(window.jQuery),
function(t) {
  "use strict";
  var i = function() {};
  i.prototype.initTooltipPlugin = function() {
    t.fn.tooltip && t('[data-toggle="tooltip"]').tooltip()
  }, i.prototype.initPopoverPlugin = function() {
    t.fn.popover && t('[data-toggle="popover"]').popover()
  }, i.prototype.initCustomModalPlugin = function() {
    t('[data-plugin="custommodal"]').on("click", function(i) {
      Custombox.open({
        target: t(this).attr("href"),
        effect: t(this).attr("data-animation"),
        overlaySpeed: t(this).attr("data-overlaySpeed"),
        overlayColor: t(this).attr("data-overlayColor")
      }), i.preventDefault()
    })
  }, i.prototype.initNiceScrollPlugin = function() {
    t.fn.niceScroll && t(".nicescroll").niceScroll({
      cursorcolor: "#98a6ad",
      cursorwidth: "6px",
      cursorborderradius: "5px"
    })
  }, i.prototype.initSlimScrollPlugin = function() {
    t.fn.slimScroll && t(".slimscroll-alt").slimScroll({
      position: "right",
      size: "5px",
      color: "#98a6ad",
      wheelStep: 10
    })
  }, i.prototype.initRangeSlider = function() {
    t.fn.slider && t('[data-plugin="range-slider"]').slider({})
  }, i.prototype.initSwitchery = function() {
    t('[data-plugin="switchery"]').each(function(i, o) {
      new Switchery(t(this)[0], t(this).data())
    })
  }, i.prototype.initMultiSelect = function() {
    t('[data-plugin="multiselect"]').length > 0 && t('[data-plugin="multiselect"]').multiSelect(t(this).data())
  }, i.prototype.initPeityCharts = function() {
    t('[data-plugin="peity-pie"]').each(function(i, o) {
      var e = t(this).attr("data-colors") ? t(this).attr("data-colors").split(",") : [],
        n = t(this).attr("data-width") ? t(this).attr("data-width") : 20,
        a = t(this).attr("data-height") ? t(this).attr("data-height") : 20;
      t(this).peity("pie", {
        fill: e,
        width: n,
        height: a
      })
    }), t('[data-plugin="peity-donut"]').each(function(i, o) {
      var e = t(this).attr("data-colors") ? t(this).attr("data-colors").split(",") : [],
        n = t(this).attr("data-width") ? t(this).attr("data-width") : 20,
        a = t(this).attr("data-height") ? t(this).attr("data-height") : 20;
      t(this).peity("donut", {
        fill: e,
        width: n,
        height: a
      })
    }), t('[data-plugin="peity-donut-alt"]').each(function(i, o) {
      t(this).peity("donut")
    }), t('[data-plugin="peity-line"]').each(function(i, o) {
      t(this).peity("line", t(this).data())
    }), t('[data-plugin="peity-bar"]').each(function(i, o) {
      var e = t(this).attr("data-colors") ? t(this).attr("data-colors").split(",") : [],
        n = t(this).attr("data-width") ? t(this).attr("data-width") : 20,
        a = t(this).attr("data-height") ? t(this).attr("data-height") : 20;
      t(this).peity("bar", {
        fill: e,
        width: n,
        height: a
      })
    })
  }, i.prototype.initKnob = function() {
    t('[data-plugin="knob"]').each(function(i, o) {
      t(this).knob()
    })
  }, i.prototype.initCircliful = function() {
    t('[data-plugin="circliful"]').each(function(i, o) {
      t(this).circliful()
    })
  }, i.prototype.initCounterUp = function() {
    t(this).attr("data-delay") ? t(this).attr("data-delay") : 100, t(this).attr("data-time") ? t(this).attr("data-time") : 1200;
    t('[data-plugin="counterup"]').each(function(i, o) {
      t(this).counterUp({
        delay: 100,
        time: 1200
      })
    })
  }, i.prototype.init = function() {
    this.initTooltipPlugin(), this.initPopoverPlugin(), this.initNiceScrollPlugin(), this.initSlimScrollPlugin(), this.initCustomModalPlugin(), this.initRangeSlider(), this.initSwitchery(), this.initMultiSelect(), this.initPeityCharts(), this.initKnob(), this.initCircliful(), this.initCounterUp(), t.Portlet.init()
  }, t.Components = new i, t.Components.Constructor = i
}(window.jQuery),
function(t) {
  "use strict";
  t.Components.init()
}(window.jQuery);
