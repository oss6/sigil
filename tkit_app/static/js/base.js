function removeClass(id_class) {
    $.ajax({
        url: "/classes/remove/" + id_class + "/"
    })
    .done(function(data) {
        location.href = "/classes/";
    });
}

function removeStudent(class_name, id_student) {
    $.ajax({
        url: "/classes/" + class_name + "/students/remove/" + id_student +"/"
    })
    .done(function(data) {
        location.href = "/classes/" + class_name + "/students/";
    });
}

function removeLesson(id_lesson) {
    $.ajax({
        url: "/lessons/remove/" + id_lesson + "/"
    })
    .done(function(data) {
        location.href = "/lessons/";
    });
}

function applyGrade(cls, id_grade, grade_value) {
    $.ajax({
        url: "/gradebook/update/" + id_grade + "/" + grade_value + "/"
    })
    .done(function(data) {
        location.href = "/classes/" + cls + "/gradebook/";
    });
}

$(document).ready(function() {
    $('.draggable').draggable();
});

/*google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawChart);

function drawChart() {
    var jsonData = $.ajax({
        url: "grades-chart/",
        dataType:"json",
        async: false
    }).responseText;

    var data = new google.visualization.DataTable(jsonData);
    var chart = new google.visualization.ColumnChart(document.getElementById('grades-chart'));
    chart.draw(data, {width: 400, height: 240});
}*/