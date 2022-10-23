function data_choice(cb, did) {
    var x = document.querySelector("#id_links");
    if (cb.checked) {
        x.value = x.value + did + ','
        x.value = x.value.replace(/,$/, '')
    }
    else {
        reg = RegExp('^' + did + ',')
        x.value = x.value.replace(reg, '')
        reg = RegExp(',' + did + '$')
        x.value = x.value.replace(reg, '')
        reg = RegExp(',' + did + ',')
        x.value = x.value.replace(reg, ',')
    }
}