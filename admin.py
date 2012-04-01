from django.contrib import admin
from models import Server, Channel, Client

class ServerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Server, ServerAdmin)
