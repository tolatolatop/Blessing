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

function post_comment() {
    var $comment_form = $('#submitModel-table');
    var comment_data =  get_comment_data($comment_form);
    var comment_link = get_comment_link();
    comment_data['link'] = comment_link;
    $.ajax({
        url: '/comments/comment',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(filter_data),
        dataType: 'json',
        success: function(result) {
            $('#submitModel').modal('hide');
            $('#table').bootstrapTable('refresh');
        }
    });
}

function get_comment_link() {
    var $table = $('#table');
    var data_list = $table.bootstrapTable('getSelections');
    var id_list = [];
    data_list.forEach((e)=>{id_list.push(e['id'])});
    return id_list
}

function get_comment_data($form) {
    var comment_data = getFormData($form)
    return comment_data
}