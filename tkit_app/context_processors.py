from tkit_app.models import ToDoList, Settings


def tasks_count(request):
    return {
        'tasks_count': len(ToDoList.objects.filter(teacher=request.user.pk, percentage__lte=99)),
    }


def first_five_tasks(request):
    return {
        'first_five_tasks':
            ToDoList.objects.filter(teacher=request.user.pk, percentage__lte=99).order_by('date_exp').reverse()[:5],
    }


def color_schema(request):
    try:
        clr = Settings.objects.get(teacher=request.user).color_scheme
    except Exception:
        clr = 'skin-blue'

    return {
        'color_schema': clr
    }