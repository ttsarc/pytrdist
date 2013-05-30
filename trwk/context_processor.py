from django.conf import settings


def admin(request):
    context_extras = {}
    if settings.ADMIN and request.user.is_superuser:
        context_extras['admin'] = True
    else:
        context_extras['admin'] = False

    return context_extras
