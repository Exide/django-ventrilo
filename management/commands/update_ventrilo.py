import subprocess
import urllib2

from django.core.management.base import BaseCommand, CommandError

from models import Server, Channel, Client


class Command(BaseCommand):
    args = '<server_host ...>'
    help = 'Queries a Ventrilo server for its status'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify a Ventrilo server id')
        for server_host in args:
            try:
                server = Server.objects.get(host=server_host)
            except Server.DoesNotExist:
                raise CommandError('Server "%s" does not exist' % server_host)

            # execute the ventrilo_status app
            command = '%s -c%d -t%s:%d' % (server.app, server.detail, server.host, server.port)
            ventrilo_status = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ventrilo_status.communicate()

            # stop now if there are errors
            if stderr:
                error_msg = '%s:%d - %s' % (server.host, server.port, stderr.strip())
                raise CommandError(error_msg)
            if 'ERROR:' in stdout[0:6]:
                error_msg = '%s:%d - %s' % (server.host, server.port, stdout.strip())
                raise CommandError(error_msg)

            # drop old data
            server.channel_set.all().delete()

            # create the lobby explicitly
            lobby = Channel(cid=0, name='Lobby', server=server)
            lobby.save()

            # iterate over the results
            for line in stdout.splitlines():
                if line.startswith('NAME:'):
                    server.name = line[6:].strip()

                if line.startswith('COMMENT:'):
                    server.comment = urllib2.unquote(line[9:].strip())

                if line.startswith('CHANNEL:'):
                    channel = Channel(server=server)
                    for attribute in line[9:].split(','):
                        key, value = attribute.split('=')
                        if key == 'CID':    channel.cid = int(value)
                        if key == 'NAME':   channel.name = value
                        if key == 'COMM':   channel.comment = urllib2.unquote(value)
                    channel.save()
                    server.channel_set.add(channel)

                if line.startswith('CLIENT:'):
                    client = Client()
                    for attribute in line[8:].split(','):
                        key, value = attribute.split('=')
                        if key == 'ADMIN':  client.admin = True if '1' in value else False
                        if key == 'NAME':   client.name = value
                        if key == 'COMM':   client.comment = urllib2.unquote(value)
                        if key == 'CID':    client.channel = server.channel_set.get(cid=value)
                    client.save()
                    client.channel.client_set.add(client)

            server.save()
            print 'Successfully updated local Ventrilo data from', server.name
