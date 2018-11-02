function replaceButtonsForReferrer() {
  var cta_placeholder = $('.buttons-cta-section');

  // if (FOR_WHO_PARA) {
  //   html = `<a href="https://meports.com/gene/provider" class="btn btn-info waves-effect w-md waves-light m-b-5" role="button"><i class="fa fa-envelope m-r-5"></i> Integrate Genetic Analysis Into Your Practice</a>`;
  //   cta_placeholder.html(html);
  //
  // } else {
  var html = `<button id="send-to-button" class="btn btn-info waves-effect w-md waves-light m-b-5"> <i class="fa fa-envelope m-r-5"></i> <span>Get an Expert Opinion</span> </button>
  <button id="delete-report-button" class="btn btn-danger waves-effect w-md waves-light m-b-5"> <i class="fa fa-trash m-r-5"></i> <span>Delete Forever</span> </button>`;
  cta_placeholder.html(html);
  // }
}


//1. get JSON from AJAX
function retrieveReportDataFromAJAX() {
  $.ajax({
    url: `/api/report/${REPORT_ID}`,
    type: "GET",
    success: function(resp) {
      initCreationTimeVar(resp.response.timestamp)
      forEachParse(resp.response.report_dict)
      console.log(resp)
    }
  });
}

//2. send each JSON to datatable
function forEachParse(report_dict) {
  var snp_array = new Array()
  //append snp dict to snp array if it contains a tag
  report_dict.forEach(function(snp) {
    // if (arrayContains(tag, snp.tag)) {
    //   // snp.gene =
      snp.snp = `${snp.rsid}:${snp.geno}`
      snp.gene_link = `<a class="gene-link" href="https://en.wikipedia.org/wiki/${snp.gene}">${snp.gene}</a>`
    // }
    snp_array.push(snp)
  })
  generateDataTable(snp_array)
}

function generateDataTable(snp_array) {
  var table_html = `
  <table id="table-genes" class="table table-striped table-bordered">
     <thead>
         <tr>
             <th>Gene</th>
             <th>Significance</th>
             <th>Summary</th>
             <th>Keyword</th>
             <th>SNP</th>
         </tr>
        </thead>
 </table>
  `
  $(`#content-placeholder`).html(table_html)

  $(`#table-genes`).DataTable({
    data: snp_array,
    columnDefs: [{
      type: 'formatted-num',
      targets: [1]
    }],
    "language": {
      "emptyTable": "No results here"
    },
    createdRow: function(row, data, dataIndex) {
      var repute = data['repute'];
      if (repute == "good" ) {
        $(row).addClass('table-row-good');
      }
      if (repute == "bad" ) {
        $(row).addClass('table-row-bad');
      }
    },
    "paging": false,
    "info": false,
    dom: "Bfrtip",
    buttons: [{
      orientation: 'portrait', //lanscape
      pageSize: 'A4', //A3 , A5 , A6 , legal , letter
      extend: "pdf",
      className: "btn-sm pdf-download",
      text: '<i class="fa fa-download"></i> Download as PDF',
      title: `office_${moment().format('MM-DD-YYYY')}`,
      exportOptions: {
        columns: ':visible',
        search: 'applied',
        order: 'applied'
      }
    }],
    columns: [{
        data: 'gene_link'
      },
      {
        data: 'mag'
      },
      {
        data: 'summary'
      },
      {
        data: 'tag'
      },
      {
        data: 'snp'
      }
    ],
    aaSorting: [1, "desc"]
  });
}

function initDeleteReportButton() {
  $("#delete-report-button").click(function(e) {
    eraseCookie('report_id');
    e.preventDefault();
    $.ajax({
      type: "DELETE",
      url: `/api/report/${REPORT_ID}`,
      success: function(result) {
        location.href = `/`;
      }
    });
  });
};

function initSendToButton() {
  $("#send-to-button").click(function(e) {
    e.preventDefault();
    $('#for-who-modal').modal('toggle');
    $("#for-who-form")[0].reset();
  });
}

function initCreationTimeVar(timestamp) {
  var creationDateVar = $('#report-creation-time');
  var momentDate = moment.unix(timestamp).format('dddd, MMMM Do, YYYY h:mm:ss A')
  if ((momentDate == 'Invalid date')) {
    creationDateVar.text('Friday, October 19 2018')

    var elem = $('#nav-report-cta')

    elem.attr("href", `/`)
    elem.text('Create Report')
    eraseCookie('report_id')

  } else {
    creationDateVar.text(momentDate)
  }

}

function initTableSpinner() {
  $(`#content-placeholder`).html(`<i class="fa fa-spin fa-spinner" style="font-size: 40px;text-align: center;width: 50%;"></i>`);
}

function initForWhoModal() {
  $("#for-who-form").on("submit", function() {
    var form = $(this);
    var elem = form.find(':submit');
    loadSpinner(elem, '', 'disable');
    $.ajax({
      type: 'POST',
      url: `/api/user`,
      data: form.serialize(),
      success: function(data) {
        loadSpinner(elem, 'Send', 'enable');
        toastr['success']('Report sent!')

        setTimeout(function() {
          $('#for-who-modal').modal('toggle');
        }, 2000);

      },
      error: function(data) {
        loadSpinner(elem, 'Send', 'enable');
        console.log(data);
      },
    });
    return false;
  })
}

//Run before load:
initTableSpinner();

//Run after load:
window.onload = function() {
  replaceButtonsForReferrer();
  initSendToButton();
  initDeleteReportButton();
  retrieveReportDataFromAJAX();
  initForWhoModal();
}
