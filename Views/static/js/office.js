var stored_genes = [];

function initTagsInput() {
  var selector = $('#keyword-search')

  selector.on('beforeItemAdd', function(event) {
    if (stored_genes.length >= 3){
      event.cancel = true;
      toastr['error']('Maximum of 3 keywords allowed')
    }
  });

  selector.on('itemAdded', function(event) {
    console.log('item added')
    searchGenes(event.item)
  });

  selector.on('itemRemoved', function(event) {
    console.log('item removed')
    removeKeyword(event.item)
  });
}

function removeKeyword(keyword){
  stored_genes.forEach(function(item, index) {
    if (item.keyword == keyword){
      stored_genes.splice(index, 1);
    }
  })
  updateGenesContainer();
}

function searchGenes(keyword) {
  $.ajax({
    url: `/api/genes/search?keyword=${keyword}`,
    type: "GET",
    success: function(resp) {
      console.log(resp)
      updateGlobalGenesDict(keyword, resp.response.response)
    }
  });
}

function updateGlobalGenesDict(keyword, resp_obj) {
  var keyword_to_gene_dict = {
    "keyword": keyword,
    "genes": []
  }

  resp_obj.forEach(function(gene) {
    keyword_to_gene_dict.genes.push(gene.gene)
  })
  stored_genes.push(keyword_to_gene_dict)
  updateGenesContainer();
}

function updateGenesContainer(){
  // TODO: load spinner
  var elem = $('#genes-placeholder');
  var input_str = '';
  elem.val(input_str);

  stored_genes.forEach(function(item) {
    input_str += `${item.genes}, `
    elem.val(input_str);
  })
  // if (stored_genes.length == 0){
  //   elem.val()
  // }
}

function initForm() {
  $("#office-form").on("submit", function() {

    //add to hidden input:
    $('#genes-hidden').val(JSON.stringify(stored_genes))

    var form = $(this);
    var elem = form.find(':submit');
    var original_elem_val = elem.html();

    var base_url = CURRENT_URL.split('/office')[0]

    loadSpinner(elem, '', 'disable');

    if (stored_genes.length == 0){
      toastr['error']("Keywords and genes needed")
      return false;
    }

    $.ajax({
      type: 'POST',
      url: `/api/office`,
      data: form.serialize(),
      success: function(data) {
        loadSpinner(elem, original_elem_val, 'enable');
        $('#office-report-url').modal('toggle');
        $('#office-report-url-input').val(`${base_url}/upload?office=${data.response}`)
      },
      error: function(data) {
        loadSpinner(elem, original_elem_val, 'enable');
        console.log(data.responseJSON.message);
      },
    });

    return false;
  })
}


window.onload = function() {
  // code goes here
  initTagsInput();
  initForm();
};
