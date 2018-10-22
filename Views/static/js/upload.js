function initUploadButton() {
  $("#upload-report-form").change(function() {
    var elem = $(this)
    processFile(elem);
  });
}

function processFile(elem) {
  var formData = new FormData(elem[0]);
  var originalVal = elem.html();
  loadSpinner(elem, 'test', 'disable');
  // appendProgressBar(elem)
  $.ajax({
    type: 'POST',
    url: '/api/report/generate',
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    success: function(data, textStatus, jqXHR){
      var reportID = data['response']
      location.href = `/report/${reportID}`
    },
    error: function(jqXHR, textStatus, errorThrown){
      toastr['error']('Invalid file, are you sure you uploaded the right one?')

      loadSpinner(elem, originalVal, 'enable')
      elem.trigger("reset");
    }
  });
}

// function appendProgressBar(elem) {
//   var html =
//     `<p>We're generating your report, it could be a while. How about we send you an email when it's ready?</p><div class="progress">
//     <div class="progress progress-lg m-b-5">
//       <div class="progress-bar progress-bar-custom" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;">
//         0%
//       </div>
//     </div>`
//   var parentTab = elem.closest('.tab-content');
//   var progressPlaceholder = parentTab.find('.progress-holder');
//   progressPlaceholder.append(html);
//   //show
//   progressPlaceholder.toggleClass('hidden')
//   streamProgress(parentTab, progressPlaceholder);
// }
//
// function streamProgress(parentTab, progressPlaceholder) {
//   var source = new EventSource("/api/file/process");
//   source.onmessage = function(event) {
//     if (event.data == '99') {
//       //hide
//       event.target.close();
//       progressPlaceholder.toggleClass('hidden')
//       initResults(parentTab)
//     }
//     $('.progress-bar').css('width', event.data + '%').attr('aria-valuenow', event.data).text(event.data);
//   }
// }


$(document).ready(function(){
  initUploadButton();
});
