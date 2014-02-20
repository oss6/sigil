$(document).ready(function() {
    $("#add_class").click(function() {
        $.ajax({
            url: "/classes/add/",
            data:
            {
                class_name: $("#class_name").val(),
                school: $("#school").val(),
                description: $("#description").text()
            }
        })
        .done(function( msg ) {
            alert( "Data Saved: " + msg );
        });
    });
});