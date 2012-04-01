from django.conf.urls.defaults import *

urlpatterns = patterns('ventrilo.views',
    (r'^(?P<server_id>\d+)/$', 'status'),
)