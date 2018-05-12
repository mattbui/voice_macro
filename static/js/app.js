function loadJSON(jsonfile){
    $.ajax({
        url: jsonfile,
        success: function(data) {
            language = data['language'];
            age_group = data['age_group'];
            rows = document.getElementById("table").rows
            for(i in rows){
                if(i > 0){
                    language_code = rows[i].cells[1].innerHTML;
                    rows[i].cells[1].innerHTML = language[language_code];
                }
            }
        }
    });
}

$(document).ready(function() {
    loadJSON("/static/json/snowboy_config.json");
})