from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Server


def status(request, server_id, template_name='ventrilo/status.html'):
    kwargs = dict()
    kwargs['server'] = Server.objects.get(pk=server_id)

    context = RequestContext(request)

    return render_to_response(template_name, kwargs, context_instance=context)
