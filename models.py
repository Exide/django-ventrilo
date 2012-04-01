from django.db.models import Model, BooleanField, ForeignKey, CharField, IntegerField, DateTimeField
from django.contrib.auth.models import User

class Server(Model):
    updated = DateTimeField(auto_now=True)
    host = CharField(max_length=64)
    port = IntegerField()
    detail = IntegerField()
    app = CharField(max_length=256)
    name = CharField(max_length=64)
    comment = CharField(max_length=64)
    
    def sorted_channels(self):
        return self.channel_set.order_by('cid')
    
    def __unicode__(self):
        return self.name

class Channel(Model):
    cid = IntegerField()
    name = CharField(max_length=64)
    comment = CharField(max_length=128)
    server = ForeignKey(Server)

    def __unicode__(self):
        return self.name

class Client(Model):
    admin = BooleanField()
    name = CharField(max_length=64)
    comment = CharField(max_length=128)
    channel = ForeignKey(Channel)

    def __unicode__(self):
        return self.name

def encode(obj):
    if isinstance(obj, Server):
        return [obj.name, obj.comment, obj.channel_set.all()]
    elif isinstance(obj, Channel):
        return [obj.name, obj.comment, obj.client_set.all()]
    elif isinstance(obj, Client):
        return [obj.name, obj.comment]
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")
