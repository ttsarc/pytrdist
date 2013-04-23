from django.conf import settings

def admin(request):
    context_extras = {}
    if settings.ADMIN and request.user.is_superuser == True:
        context_extras['admin'] = True
    return context_extras
