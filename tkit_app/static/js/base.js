var mitem = {
    removeItem: function(id_item) {
       $.ajax({
            url: "/todolist/remove/" + id_item + "/"
       })
       .done(function(data) {
            location.href = "/todolist/";
       });
    }
};

var mgrade = {
    applyGrade: function(id_class, id_grade, grade_value) {
        $.ajax({
            url: "/gradebook/update/" + id_grade + "/" + grade_value + "/"
        })
        .done(function(data) {
            location.href = "/classes/" + id_class + "/gradebook/";
        });
    },

    drawGradesChart: function() {
        var jsonData = $.ajax({
            url: "grades-chart/",
            dataType:"json",
            async: false
        }).responseText;

        var data = new google.visualization.DataTable(jsonData);
        var chart = new google.visualization.ColumnChart(document.getElementById('grades-chart'));
        chart.draw(data, {width: 400, height: 240});
    },

    drawPerformance: function() {
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
};

var mattendance = {
    applyAttendance: function(id_class, date, id_att, att_type) {
        $.ajax({
            url: "/attendance/update/" + id_att + "/" + att_type + "/"
        })
        .done(function(data) {
            location.href = "/classes/" + id_class + "/attendance/" + date + "/";
        });
    },

    changeDateAtt: function(id_class, date) {
        location.href = "/classes/" + id_class + "/attendance/" + date + "/";
    },

    drawAttendanceChart: function() {
        var jsonData = $.ajax({
            url: "attendance-chart/",
            dataType:"json",
            async: false
        }).responseText;

        var data = new google.visualization.DataTable(jsonData);
        var options = {
            title: 'Attendance',
            pieHole: 0.4,
        };

        var chart = new google.visualization.PieChart(document.getElementById('attendance-chart'));
        chart.draw(data, options);
    }
};

var mnote = {
    drawNotesChart: function() {
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
};

var utils = {
    postData: function(url, data, redirect) {
        $.post(url, data, function() {
            location.href = redirect;
        }, 'html');
    }
};

$(document).ready(function() {
    $(".date").datepicker();

    // CLASSES
    $("#addClass").click(function() {
        $('#addClassModal').modal('show');
        return false;
    });

    $("#addClassModalSave").click(function() {
        utils.postData("/classes/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            name: $("#name").val(),
            school: $("#school").val(),
            description: $("#desc").val(),
        }, "/classes/");
    });

    // STUDENTS
    $("#addStudent").click(function() {
        $('#addStudentModal').modal('show');
        return false;
    });

    $("#addStudentModalSave").click(function() {
        utils.postData("/classes/" + $(this).attr("data-class") + "/students/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            first_name: $("#first_name").val(),
            last_name: $("#last_name").val(),
            email: $("#email").val(),
            parent: $("#parent").val(),
            parent_email: $("#parent_email").val(),
            photo: $("#photo").val(),
        }, "/classes/" + $(this).attr("data-class") + "/students/");
    });

    // GRADE BOOK
    $("#addGrade").click(function() {
        $('#addGradeModal').modal('show');
        return false;
    });

    $("#addGradeModalSave").click(function() {
        utils.postData("/classes/" + $(this).attr("data-class") + "/gradebook/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            title: $("#title").val(),
            description: $("#description").val(),
            date_begin: $("#date_begin").val(),
            date_end: $("#date_end").val(),
        }, "/classes/" + $(this).attr("data-class") + "/gradebook/");
    });

    // LESSONS
    $("#addLesson").click(function() {
        $('#addLessonModal').modal('show');
        return false;
    });

    $("#addLessonModalSave").click(function() {
        utils.postData("/lessons/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            title: $("#title").val(),
            description: $("#desc").val(),
            date: $("#date").val()
        }, "/lessons/");
    });

    // ASSIGNMENTS
    $("#addAssignment").click(function() {
        $('#addAssignmentModal').modal('show');
        return false;
    });

    $("#addAssignmentModalSave").click(function() {
        utils.postData("/classes/" + $(this).attr("data-class") + "/gradebook/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            subject: $("#subject").val(),
            date: $("#date").val(),
            type: $("#type").val(),
        }, "/classes/" + $(this).attr("data-class") + "/gradebook/");
    });

    // LIST ITEMS
    $("#addListItem").click(function() {
        $("#addListItemModal").modal("show");
        return false;
    });

    $("#addListItemModalSave").click(function() {
        utils.postData("/todolist/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            title: $("#title").val(),
            date_exp: $("#date").val(),
            perc: $("#perc").val()
        }, "/todolist/");
    });
});

/*google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(mgrade.drawGradesChart);
google.setOnLoadCallback(mnote.drawNotesChart);
google.setOnLoadCallback(mattendance.drawAttendanceChart);
//google.setOnLoadCallback(mgrade.drawPerformance);*/