function removeClass(class_name) {
    $.ajax({
        url: "/classes/remove/" + class_name + "/"
    })
    .done(function(data) {
        console.log(data);
    });
}

function removeStudent(class_name, id_student) {
    $.ajax({
        url: "/classes/" + class_name + "/students/remove/" + id_student +"/"
    })
    .done(function(data) {
        console.log(data);
    });
}