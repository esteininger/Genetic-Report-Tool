//GLOBAL VARS:
var FOR_WHO_PARA = getParameterByName('for');
var TAG_FILTERS = ['beneficial', 'noteworthy', 'acmg'];

function replaceButtonsForReferrer() {
  var cta_placeholder = $('.buttons-cta-section');
  if (FOR_WHO_PARA) {
    html = `<a href="https://meports.com/gene/provider" class="btn btn-info waves-effect w-md waves-light m-b-5" role="button"><i class="fa fa-envelope m-r-5"></i> Integrate Genetic Analysis Into Your Practice</a>`;
    cta_placeholder.html(html);
  } else {
    var html = `<button id="send-to-button" class="btn btn-info waves-effect w-md waves-light m-b-5"> <i class="fa fa-envelope m-r-5"></i> <span>Get an Expert Opinion</span> </button>
    <button id="delete-report-button" class="btn btn-danger waves-effect w-md waves-light m-b-5"> <i class="fa fa-trash m-r-5"></i> <span>Delete Forever</span> </button>`;
    cta_placeholder.html(html);
  }
}

function updateNav() {
  var elem = $('#nav-report-cta')
  //does url parameter for_who exist?
  if (FOR_WHO_PARA) {
    elem.attr("href", `/`)
    elem.text('Integrate Today')
  } else if (REPORT_IS_VALID == 'True') {
    //report exists in session, change URL to report ID
    elem.attr("href", `/report/${REPORT_ID}`)
    elem.text('My Report')
    setCookie('report_id', REPORT_ID, 2)
  }
}


//1. get JSON from AJAX
function retrieveReportDataFromAJAX() {
  $.ajax({
    url: `/api/report/${REPORT_ID}`,
    type: "GET",
    success: function(resp) {
      initCreationTimeVar(resp.response.timestamp)
      forEachParse(resp.response.report_dict)
    },
    error: function(resp) {
      var elem = $('#nav-report-cta')
      elem.attr("href", `/`)
      elem.text('Create Report')
      eraseCookie('report_id')
    }
  });
}

//2. send each JSON to datatable
function forEachParse(report_dict) {
  //loop all tags
  TAG_FILTERS.forEach(function(tag) {

    var snp_array = new Array()
    //append snp dict to snp array if it contains a tag
    report_dict.forEach(function(snp) {
      if (arrayContains(tag, snp.tag)) {
        snp.link = `<a href="https://en.wikipedia.org/wiki/${snp.gene}">Link</a>`
        snp_array.push(snp)
      }
    })
    //send snp array to datatable creation function
    generateDataTable(snp_array, tag)
  });
}

function generateDataTable(snp_array, tag) {
  var table_html = `
  <table id="table-${tag}" class="table table-striped table-bordered">
     <thead>
         <tr>
             <th>Gene</th>
             <th>Significance</th>
             <th>Reputation</th>
             <th>Link</th>
         </tr>
        </thead>
 </table>
  `
  $(`#table-${tag}-placeholder`).html(table_html)

  $(`#table-${tag}`).DataTable({
    data: snp_array,
    columnDefs: [{
      type: 'formatted-num',
      targets: [1]
    }],
    "paging": false,
    "info": false,
    buttons: [{
      extend: "pdf",
      className: "btn-sm"
    }],
    columns: [{
        data: 'gene'
      },
      {
        data: 'mag'
      },
      {
        data: 'repute'
      },
      {
        data: 'link'
      }
    ],
    aaSorting: [1, "desc"]
  });
}

function initDeleteReportButton() {
  $("#delete-report-button").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "DELETE",
      url: `/api/report/${REPORT_ID}`,
      success: function(result) {
        location.href = `/`
      },
      error: function(result) {
        toastr['error'](result.message)
      }
    });
  });
};

function initSendToButton() {
  $("#send-to-button").click(function(e) {
    e.preventDefault();
    $('#for-who-modal').modal('toggle');
  });
}

function initCreationTimeVar(timestamp) {
  var creationDateVar = $('#report-creation-time');
  var momentDate = moment.unix(timestamp).format('dddd, MMMM Do, YYYY h:mm:ss A')
  if (momentDate == 'Invalid date') {
    creationDateVar.text('the beginning...')

    var elem = $('#nav-report-cta')
    
    elem.attr("href", `/report/${REPORT_ID}`)
    elem.text('Create Report')
    eraseCookie('report_id')

  } else {
    creationDateVar.text(momentDate)
  }

}

function initTableSpinner() {
  TAG_FILTERS.forEach(function(entry) {
    $(`#table-${entry}-placeholder`).html(`<i class="fa fa-spin fa-spinner" style="font-size: 40px;text-align: center;width: 50%;"></i>`);
  });
}

//Run before load:
updateNav();
initTableSpinner();

//Run after load:
window.onload = function() {
  replaceButtonsForReferrer();
  initSendToButton();
  initDeleteReportButton();
  retrieveReportDataFromAJAX();
}
