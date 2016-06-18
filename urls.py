from django.conf.urls import patterns

urlpatterns = patterns('ventrilo.views',
                       (r'^(?P<server_id>\d+)/$', 'status'),
                       )
