function loadJSON(jsonfile, language_select, age_select){
    $.ajax({
        url: jsonfile,
        success: function(data) {
            language = data['language'];
            age_group = data['age_group'];
            language_html = "";
            keys = Object.keys(language)
            for(i in keys){
                language_html += "<option value='" + keys[i] + "'>" + language[keys[i]] + "</option>";
            }
            age_html = "";
            for(i in age_group) {
                age_html += "<option value='" + age_group[i] + "'>" + age_group[i] + "</option>";
            }
            $(age_select).html(age_html);
            $(language_select).html(language_html);
        }
    });
}

$(document).ready(function() {
    loadJSON("/static/json/snowboy_config.json", "#language", "#age");

    $("#cancel").on("click", (function(e) {
        form = new FormData()
        form.append("sound_1", $("#sound-1").attr("sound-file"));
        form.append("sound_2", $("#sound-2").attr("sound-file"));
        form.append("sound_3", $("#sound-3").attr("sound-file"));
        form.append("key_file", $("#key-record-btn").attr("key-file"));

        $.ajax({
            url: '/clear_cache',
            type: "POST",
            data: form,
            dataType: 'json',
            contentType: false,
            cache: false,
            processData:false,
            success: function(data) {
                window.location.href = "/";
            }
        });
    }));
    
    $(".sound-record-btn").on("click", (function(e) {
        id = "#" + $(this).attr("id")
        $.ajax({
            url: '/switch_sound_record',
            success: function(data) {
                if(data["message"] == "recording") {
                    $(id).removeClass("btn-recorded");
                    $(id).removeClass("btn-no-record");
                    $(id).addClass("btn-recording");
                    $(id).html("Recording");
                }
                else {
                    $(id).removeClass("btn-recording");
                    $(id).removeClass("btn-no-record");
                    $(id).addClass("btn-recorded");
                    $(id).html("Recorded");
                    $(id).attr("sound-file", data['message']);
                    console.log($(id).attr("sound-file"));
                }
            }
        });
    }));

    $("#key-record-btn").on("click", (function(e) {
        if($(this).html() == "Recording") return false;
        $(this).html("Recording")
        $(this).removeClass("btn-recorded");
        $(this).removeClass("btn-no-record");
        $(this).addClass("btn-recording");
        file =  $("#key-record-btn").attr("key-file")
        form = new FormData()
        form.append("file", file)

        $.ajax({
            url: '/keyboard_record',
            type: "POST",
            data: form,
            dataType: 'json',
            contentType: false,
            cache: false,
            processData:false,
            success: function(data) {
                $("#key-record-btn").html("Recorded")
                $("#key-record-btn").removeClass("btn-recording");
                $("#key-record-btn").removeClass("btn-no-record");
                $("#key-record-btn").addClass("btn-recorded");
                output_file = data["output_file"];
                events_string = data["events_string"];
                $("#key-record-btn").attr("key-file", output_file);
                $("#key-event").html(events_string);
            }
        });
    }));

    $("#macro-form").on('submit',(function(e) {
        e.preventDefault();
        if($("#create_macro").val() == "Training") {
            return false;
        }
        if($("#sound-1").attr("sound-file") == "" || $("#sound-2").attr("sound-file") == "" || $("#sound-3").attr("sound-file") == "") {
            alert("Please record 3 sound files before submit")
        }
        if($("#key-record-btn").attr("key-file") == "") {
            alert("Please record macro before submit")
        }
        else {
            form = new FormData(this);
            form.append("sound_1", $("#sound-1").attr("sound-file"));
            form.append("sound_2", $("#sound-2").attr("sound-file"));
            form.append("sound_3", $("#sound-3").attr("sound-file"));
            form.append("key_file", $("#key-record-btn").attr("key-file"));
            form.append("events_string", $("#key-event").html());
            $("#create_macro").val("Training")
            $("#create_macro").addClass("btn-no-record")
            $("#create_macro").removeClass("gradient-border")
            $.ajax({
                url: "/add_macro", 
                type: "POST",
                data: form,
                dataType: 'json',
                contentType: false,
                cache: false,
                processData:false,
                success: function(data) {
                    message = data['message']
                    if(message == "ok"){
                        window.location.href = "/";
                    }
                    else {
                        alert(message);
                        $("#create_macro").val("Submit")
                        $("#create_macro").removeClass("btn-no-record")
                        $("#create_macro").addClass("gradient-border")
                    }
                },
            });
        }
    }));
})