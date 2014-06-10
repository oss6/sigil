var utils = {
    getCookie: function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    postData: function(url, data, redirect) {
        $.post(url, data, function() {
            location.href = redirect;
        });
    },

    postJSONData: function(url, JSONData, redirect) {
        var fn = $("#json-file-name").val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                json_data: JSONData,
                file_name: fn
            },
            success: function(data){
                location.href = redirect
            },
            error: function(x, status, error) {
                if (x.status != 403) {
                    console.log("An error occurred: " + status + "nError: " + error);
                }
            }
         });
    }
};