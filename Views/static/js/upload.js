var OFFICE_PARA = getParameterByName('office');

function initUploadButton() {
  $("#upload-report-form").change(function() {
    var elem = $(this)
    processFile(elem);
  });
}

function initSourceSelector() {
  $("#source-selector").on('change', function() {
    var source = this.value
    updateSourceHelper(source);
  });

}

function updateSourceHelper(source) {
  var source_to_url = {
    "23andme": "https://customercare.23andme.com/hc/en-us/articles/212196868-Accessing-and-Downloading-Your-Raw-Data",
    "ancestry": "https://support.ancestry.com/s/article/Downloading-Raw-DNA-Data-1460089696533",
    "ftdna": "https://www.familytreedna.com/learn/user-guide/family-finder-myftdna/download-raw-data-page/",
    "other":""
  }

  var html;

  if (source == 'other') {
    html = `<p>Don't see your genetic testing provider? <a href="mailto:ethan@meports.com">Email us</a> and we'll make it work!</p>`
  } else {
    html = `<p>Don't have a ${source} genome file? Download yours <a class="bolded" href="${source_to_url[source]}">here</a></p>`
  }

  $('#source-helper').html(html);
}

function processFile(elem) {
  var formData = new FormData(elem[0]);
  var originalVal = elem.html();
  var placeholder = $('.upload-holder');
  loadSpinner(elem, 'test', 'disable');
  initLoadText(elem)
  // appendProgressBar(elem)
  var source = $('#source-selector').val()

  var full_url = `/api/report/generate?source=${source}`

  if (OFFICE_PARA) {
    full_url += `&office=${OFFICE_PARA}`
  }

  $.ajax({
    type: 'POST',
    url: full_url,
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    success: function(data, textStatus, jqXHR) {
      var reportID = data['response']
      setCookie('report_id', reportID, 2)
      location.href = `/report/${reportID}`
    },
    error: function(jqXHR, textStatus, errorThrown) {
      toastr['error']('Invalid file, are you sure you uploaded the right one?')

      loadSpinner(elem, originalVal, 'enable')
      elem.trigger("reset");
    }
  });
}

function initLoadText(elem) {
  elem.append(`<div id="rotate"> <div>Your genome is most likely over 16,000 kbs, it may take a couple minutes.</div> <div>We're just comparing your genome to our list of genes.</div> <div>Is it still running? Hmmm, keep this window open and carry on...</div> </div>`)
  $('#rotate').rotaterator({
    fadeSpeed: 2000,
    pauseSpeed: 2000
  });
}

//1. get JSON from AJAX
function initGenesWeLookForButton() {
  $("#genes-we-look-for-button").click(function(e) {
    e.preventDefault();
    $('#genes-we-look-for').modal('toggle');

    $.ajax({
      url: `/api/report/genes`,
      type: "GET",
      success: function(resp) {
        generateDataTable(resp.response)
      }
    });
  });
}


function generateDataTable(data) {
  // var arr = new Array()
  //append snp dict to snp array if it contains a tag
  data.forEach(function(d) {
    d.gene = `<a class="gene-link" href="https://en.wikipedia.org/wiki/${d.gene}">${d.gene}</a>`
  })

  $(`#gene-table-placeholder`).DataTable({
    data: data,
    columns: [{
        data: 'gene'
      },
      {
        data: 'description'
      },
      {
        data: 'tag'
      }
    ],
    aaSorting: [1, "desc"]
  });

  $('#genes-we-look-for').on('hidden.bs.modal', function() {
    $('#gene-table-placeholder').dataTable().fnDestroy();
  })
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


$(document).ready(function() {
  initUploadButton();
  initGenesWeLookForButton();
  initSourceSelector();
});
