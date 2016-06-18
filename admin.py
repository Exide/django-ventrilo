from django.contrib import admin

from models import Server


class ServerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Server, ServerAdmin)
