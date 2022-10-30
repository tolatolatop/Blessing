$('#submitModel').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
})


function getFormData($form){
    var un_indexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(un_indexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function get_filter_data() {
    var ele = $("#filterModel-table");
    var data = getFormData(ele)
    var filter_data = {}
    for (var key in data) {
        if (key != 'csrfmiddlewaretoken' && data[key] != "") {
            filter_data[key + '__contains'] = data[key]
        }
    }
    return filter_data
}

function save_filter() {
    var filter_data = get_filter_data();
    $.ajax({
        url: '/comments/save_filter',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(filter_data),
        dataType: 'json',
        success: function(result) {
            $('#filterModel').modal('hide');
            $('#table').bootstrapTable('refresh');
        }
    });
}

