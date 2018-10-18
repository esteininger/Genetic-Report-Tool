// function loadDataForLogTable() {
//   var placeholder = $('#table-loader-placeholder');
//   placeholder.html(`<i class="fa fa-spin fa-spinner" style="font-size: 40px;text-align: center;width: 50%;"></i>`);
//   $.ajax({
//     url: "/api/log",
//     type: "GET",
//     success: function(resp) {
//       placeholder.html(`
//         <div class="table-responsive">
//           <table id="datatable" class="table table-striped table-bordered">
//             <thead>
//               <tr>
//                 <th>snapshot</th>
//                 <th>person</th>
//                 <th>group</th>
//                 <th>camera</th>
//                 <th>timestamp</th>
//                 <th>action</th>
//               </tr>
//             </thead>
//           </table>
//         </div>
//         `)
//       ajaxResult(resp.response);
//     }
//   });
// }

//build table:

function buildTableStr(){
  $(reportJSON.report_dict).each(function(key, value) {
    $('<tr>').append(
        $('<td>').text(value.gene),
        $('<td>').text(value.mag),
        $('<td>').text(value.summary)
    ).appendTo('#acmg-tbody');
  });
};

function initDeleteReportButton(){
  $("#delete-report-button").click(function(e) {
      e.preventDefault();
      $.ajax({
          type: "DELETE",
          url: `/report/${reportJSON.report_id}`,
          success: function(result) {
            location.href = `/`
          },
          error: function(result) {
              toastr['error'](result.message)
          }
      });
  });
};

function initSendToButton(){
  $("#send-to-button").click(function(e) {
      e.preventDefault();
      $('#for-who-modal').modal('toggle');
  });
}

// $(planJSON).each(function(key, value) {
//     planLabels.push(this['symbol'])
//     planData.push( (parseFloat(this['percent']) * 100).toFixed(2) )
//     planDescriptions.push(this['description'])
// });


function initCreationTimeVar(){
  var creationDateVar = $('#report-creation-time');
  var momentDate = moment.unix(reportJSON.timestamp).format('dddd, MMMM Do, YYYY h:mm:ss A')
  if (momentDate == 'Invalid date'){
    creationDateVar.text('the beginning...')
  }
  else{
    creationDateVar.text(momentDate)
  }

}

//wrap everything with onload because this is being run before jQuery init
window.onload = function(){
  initSendToButton();
  buildTableStr();
  initDeleteReportButton();
  initCreationTimeVar();
}
