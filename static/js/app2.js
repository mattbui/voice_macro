function loadJSON(jsonfile){
    $.ajax({
        url: jsonfile,
        success: function(data) {
            language = data['language'];
            age_group = data['age_group'];
            l = $("#language").html();
            $("#language").html(language[l])
            g = $("#gender").html();
            if(g == "M") {
                $("#gender").html("Male")
            }
            else if(g == "F") {
                $("#gender").html("Female")
            }
        }
    });
}

$(document).ready(function() {
    loadJSON("/static/json/snowboy_config.json");
})