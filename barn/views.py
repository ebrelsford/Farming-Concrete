from django.conf import settings
from django.http import HttpResponseServerError
from django.template import Context, loader

def server_error(request, template_name='500.html'):
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))
