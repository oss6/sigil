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
        events.push({ date: obj.date_exp, title: obj.title });
    }

    for (i = 0; i < LESSONS_OBJ.length; i++) {
        obj = LESSONS_OBJ[i].fields
        events.push({ date: obj.date, title: obj.title });
    }

    for (i = 0; i < ASSIGNMENTS_OBJ.length; i++) {
        obj = ASSIGNMENTS_OBJ[i].fields
        events.push({ date: obj.date_end, title: obj.title });
    }

    // Calendar
    $('#mini-clndr').clndr({
        template: $('#mini-clndr-template').html(),
        events: events,

        clickEvents: {
            click: function(target) {
                if(target.events.length) {
                    var daysContainer = $('#mini-clndr').find('.days-container');
                    daysContainer.toggleClass('show-events', true);
                    $('#mini-clndr').find('.x-button').click( function() {
                        daysContainer.toggleClass('show-events', false);
                    });
                }
            }
        },
        adjacentDaysChangeMonth: true
    });
});