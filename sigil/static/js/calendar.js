$(document).ready(function() {
    var TODOS_OBJ = JSON.parse(TODOS),
        LESSONS_OBJ = JSON.parse(LESSONS),
        ASSIGNMENTS_OBJ = JSON.parse(ASSIGNMENTS),
        events = [],
        obj = null,
        i = 0;

    // Creating events
    for (i = 0; i < TODOS_OBJ.length; i++) {
        obj = TODOS_OBJ[i].fields
        events.push({ date: obj.date_exp, title: obj.title, type: 'Task' });
    }

    for (i = 0; i < LESSONS_OBJ.length; i++) {
        obj = LESSONS_OBJ[i].fields
        events.push({ date: obj.date, title: obj.title, type: 'Lezione' });
    }

    for (i = 0; i < ASSIGNMENTS_OBJ.length; i++) {
        obj = ASSIGNMENTS_OBJ[i].fields
        events.push({ date: obj.date_end, title: obj.title, type: 'Compito' });
    }

    $('.cal1').clndr({
        events: events,
        clickEvents: {
            click: function(target) {
                if(target.events.length) {
                    var evs = '<ul>';
                    for (var i = 0; i < target.events.length; i++)
                        evs += '<li>' + target.events[i].title + ' (' + target.events[i].type + ')</li>';
                    evs += '</ul>';

                    $("#modalDesc").html(evs);
                    $('#modal').modal('show');
                }
            }
        },
        multiDayEvents: {
            startDate: 'startDate',
            endDate: 'endDate'
        },
        showAdjacentMonths: true,
        adjacentDaysChangeMonth: false
    });
});