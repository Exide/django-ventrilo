from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Server

def status(request, server_id):
    return render_to_response(
        'ventrilo/status.html',
        {'server': Server.objects.get(pk=server_id) },
        context_instance=RequestContext(request))