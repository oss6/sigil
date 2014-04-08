function removeClass(id_class) {
    $.ajax({
        url: "/classes/remove/" + id_class + "/"
    })
    .done(function(data) {
        location.href = "/classes/";
    });
}

function removeStudent(id_class, id_student) {
    $.ajax({
        url: "/classes/" + id_class + "/students/remove/" + id_student +"/"
    })
    .done(function(data) {
        location.href = "/classes/" + id_class + "/students/";
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

function removeAssignment(id_class, id_assm) {
    $.ajax({
        url: "/classes/" + id_class + "/homework/remove/" + id_assm + "/"
    })
    .done(function(data) {
        location.href = "/classes/" + id_class + "/homework/";
    });
}

function applyGrade(id_class, id_grade, grade_value) {
    $.ajax({
        url: "/gradebook/update/" + id_grade + "/" + grade_value + "/"
    })
    .done(function(data) {
        location.href = "/classes/" + id_class + "/gradebook/";
    });
}

function drawGradesChart() {
    var jsonData = $.ajax({
        url: "grades-chart/",
        dataType:"json",
        async: false
    }).responseText;

    var data = new google.visualization.DataTable(jsonData);
    var chart = new google.visualization.ColumnChart(document.getElementById('grades-chart'));
    chart.draw(data, {width: 400, height: 240});
}

function drawPerformance() {
    var jsonData = $.ajax({
        url: "grades-performance-chart/",
        dataType:"json",
        async: false
    }).responseText;

    /*var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses'],
          ['2004',  1000,      400],
          ['2005',  1170,      460],
          ['2006',  660,       1120],
          ['2007',  1030,      540]
    ]);*/

    var options = {
        title: 'Student Performance'
    };

    var chart = new google.visualization.LineChart(document.getElementById('performance-chart'));
    chart.draw(data, options);
}

function drawNotesChart() {
    var jsonData = $.ajax({
        url: "notes-chart/",
        dataType:"json",
        async: false
    }).responseText;

    var data = new google.visualization.DataTable(jsonData);
    var options = {
        title: 'Note',
        pieHole: 0.4,
    };

    var chart = new google.visualization.PieChart(document.getElementById('notes-chart'));
    chart.draw(data, options);
}

/*google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawGradesChart);
google.setOnLoadCallback(drawNotesChart);*/
//google.setOnLoadCallback(drawPerformance);

$(document).ready(function() {
    $('.draggable').draggable();
});
