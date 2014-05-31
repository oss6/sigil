$(document).ready(function() {
    var TODOS_OBJ = JSON.parse(TODOS);
    var events = []

    // Creating events
    for (var i = 0; i < TODOS_OBJ.length; i++) {
        var obj = TODOS_OBJ[i].fields

        events.push({ date: obj.date_exp, title: obj.title });
    }

    // Calendar
    $('#mini-clndr').clndr({
        template: $('#mini-clndr-template').html(),
        events: events,
        daysOfTheWeek: ['D', 'L', 'M', 'M', 'G', 'V', 'S'],
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