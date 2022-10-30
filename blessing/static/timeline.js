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