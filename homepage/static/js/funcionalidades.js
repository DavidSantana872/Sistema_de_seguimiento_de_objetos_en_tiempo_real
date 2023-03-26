var values_selected;
window.onload = function() {
    values_selected = new Set();
}

function disableSelectedOption(select) {
    var value = select.value;
    var selects = document.getElementsByTagName('select');
    values_selected.add(value)
    console.log(select)
    console.log(select.name)
    for (var i = 0; i < selects.length; i++) {
        var options = selects[i].getElementsByTagName('option');
        let values_Array = Array.from(values_selected);
        for (var j = 0; j < options.length; j++) {
            for (var z = 0; z < values_Array.length; z++) {
                if (values_Array[z] === options[j].value && select.name != selects[i].name && selects[i].value != values_Array[z]) {
                    options[j].disabled = true;
                }
            }
        }
    }
    let elementoSiguiente = select.nextElementSibling;
    elementoSiguiente.style.display = 'flex'

}