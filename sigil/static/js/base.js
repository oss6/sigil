var mclass = {
    openClassModal: function(id_class) {
        id_class = id_class || "add";

        $("#classModalLabel").text(id_class === "add" ? "Aggiungi classe" : "Modifica classe");
        $('#addClassModal')
            .modal('show')
            .attr("data-type", id_class);
    },

    drawPerformance: function() {
        var jsonData = $.ajax({
            url: "grades-performance-chart/",
            dataType:"json",
            async: false
        }).responseText;

        var options = {
            title: 'Andamento voti'
        };

        var data = new google.visualization.DataTable(jsonData);
        var chart = new google.visualization.LineChart(document.getElementById('performance-chart'));
        chart.draw(data, options);
    }
};

var mpub = {
    openPubModal: function() {
        $('#addPubModal').modal('show');
    }
}

var mstudent = {
    openStudentModal: function(id_class, id_student) {
        id_student = id_student || "add";

        $("#student-form")
        .attr("action", id_student === "add" ? "/classes/" + id_class + "/students/add/" : "/classes/" + id_class + "/students/update/" + id_student + "/");
        $("#studentModalLabel").text(id_student === "add" ? "Aggiungi studente" : "Modifica studente");
        $("#addStudentModal").modal("show");
    }
}

var massignment = {
    openAssignmentModal: function(id_assignment) {
        id_assignment = id_assignment || "add";

        $("#addAssignmentModal")
            .modal("show")
            .attr("data-type", id_assignment);
    }
}

var mlesson = {
    openLessonModal: function(id_lesson) {
        id_lesson = id_lesson || "add";

        $('#addLessonModal')
            .modal('show')
            .attr("data-type", id_lesson);
    }
}

var mitem = {
    openItemModal: function(id_item) {
        id_item = id_item || "add";

        $('#addListItemModal')
            .modal('show')
            .attr("data-type", id_item);
    }
}

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

        var options = {
            title: 'Andamento voti'
        };

        var data = new google.visualization.DataTable(jsonData);
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

$(document).ready(function() {
    $("input[data-date-format='yyyy-mm-dd']").datepicker();

    // CLASSES
    $("#addClassModalSave").click(function() {
        var url = $("#addClassModal").attr("data-type") === "add" ? "/classes/add/" : "/classes/update/" +
        $("#addClassModal").attr("data-type") + "/";

        utils.postData(url, {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            name: $("#name").val(),
            school: $("#school").val(),
            description: $("#desc").val(),
        }, "/classes/");
    });

    // GRADE BOOK
    $("#addGrade").click(function() {
        $('#addGradeModal').modal('show');
        return false;
    });

    $("#addGradeModalSave").click(function() {
        utils.postData("/classes/" + $(this).attr("data-class") + "/gradebook/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            subject: $("#subject").val(),
            date: $("#date").val(),
            type: $("#type").val(),
        }, "/classes/" + $(this).attr("data-class") + "/gradebook/");
    });

    // NOTES
    $("#addNote").click(function() {
        $('#addNoteModal').modal('show');
        return false;
    });

    $("#addNoteModalSave").click(function() {
        utils.postData("/students/" + $(this).attr("data-student") + "/notes/add/", {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            positive: $("#positive").val(),
            date: $("#date").val(),
            comment: $("#comment").val(),
        }, "/students/" + $(this).attr("data-student") + "/");
    });

    // LESSONS
    $("#addLessonModalSave").click(function() {
        var url = $("#addLessonModal").attr("data-type") === "add" ? "/lessons/add/" : "/lessons/update/" +
        $("#addLessonModal").attr("data-type") + "/";

        utils.postData(url, {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            title: $("#title").val(),
            description: $("#desc").val(),
            date: $("#date").val()
        }, "/lessons/");
    });

    // ASSIGNMENTS
    $("#addAssignmentModalSave").click(function() {
        var id_class = $("#helper-class").val();
        var url = $("#addAssignmentModal").attr("data-type") === "add" ? "/classes/" + id_class +
        "/homework/add/" : "/classes/" + id_class + "/homework/update/" + $("#addAssignmentModal").attr("data-type") + "/";

        utils.postData(url, {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            title: $("#title").val(),
            description: $("#description").val(),
            date_begin: $("#date_begin").val(),
            date_end: $("#date_end").val(),
        }, "/classes/" + id_class + "/homework/");
    });

    // LIST ITEMS
    $("#addListItemModalSave").click(function() {
        var url = $("#addListItemModal").attr("data-type") === "add" ? "/todolist/add/" : "/todolist/update/" +
        $("#addListItemModal").attr("data-type") + "/";

        utils.postData(url, {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            title: $("#title").val(),
            date_exp: $("#date").val(),
            perc: $("#perc").val()
        }, "/todolist/");
    });
});