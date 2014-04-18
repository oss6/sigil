from tkit_app.models import ToDoList, Settings


def color_schema(request):
    try:
        clr = Settings.objects.get(teacher=request.user).color_scheme
    except Exception:
        clr = 'skin-blue'

    return {
        'color_schema': clr
    }


def tasks_count(request):
    return {
        'tasks_count': len(ToDoList.objects.filter(teacher=request.user.pk, percentage__lte=99)),
    }


def first_five_tasks(request):
    return {
        'first_five_tasks':
            ToDoList.objects.filter(teacher=request.user.pk, percentage__lte=99).order_by('date_exp').reverse()[:5],
    }


def absence_limit(request):
    try:
        labs = Settings.objects.get(teacher=request.user).absence_limit
    except Exception:
        labs = 60

    return {
        'absence_limit': labs
    }


def spc_limit(request):
    try:
        lspc = Settings.objects.get(teacher=request.user).spc_limit
    except Exception:
        lspc = 30

    return {
        'spc_limit': lspc
    }


def negative_notes_limit(request):
    try:
        lnn = Settings.objects.get(teacher=request.user).negative_notes_limit
    except Exception:
        lnn = 30

    return {
        'negative_notes_limit': lnn
    }