function removeClass(class_name) {
    $.ajax({
        url: "/classes/remove/" + class_name + "/"
    })
    .done(function(data) {
        console.log(data);
    });
}