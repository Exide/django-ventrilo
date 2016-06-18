import subprocess
import urllib2


class Channel(object):
    id = 0
    name = None
    comment = None


class Client(object):
    admin = False
    name = None
    comment = None
    channel = None


class Server(object):
    channels = dict()
    clients = list()

    def __init__(self, host='localhost', port=3184, app='./ventrilo_status'):
        self.host = host
        self.port = port
        self.app = app

    def query(self, detail=0):
        command = '%s -c%d -t%s:%d' % (self.app, detail, self.host, self.port)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        # stop now if there are errors
        if stderr:
            return None

        if 'ERROR:' in stdout[0:6]:
            return None

        # create the lobby explicitly
        c = Channel()
        c.name = 'Lobby'
        self.channels[c.id] = c

        for line in stdout.splitlines():

            if line.startswith('CHANNEL:'):

                # instantiate a channel
                c = Channel()

                # iterate over the attributes
                for attribute in line[9:].split(','):
                    key, value = attribute.split('=')

                    # set member data
                    if key == 'CID':
                        c.id = int(value)
                    if key == 'NAME':
                        c.name = value
                    if key == 'COMM':
                        c.comment = urllib2.unquote(value)

                self.channels[c.id] = c

            if line.startswith('CLIENT:'):

                # instantiate a client
                c = Client()

                # iterate over the attributes
                for attribute in line[8:].split(','):
                    key, value = attribute.split('=')

                    # set member data
                    if key == 'ADMIN':
                        c.admin = True if '1' in value else False
                    if key == 'NAME':
                        c.name = value
                    if key == 'COMM':
                        c.comment = urllib2.unquote(value)
                    if key == 'CID':
                        c.channel = int(value)

                # add the client to our list
                self.clients.append(c)


def encode(obj):
    if isinstance(obj, Server):
        return [obj.channels, obj.clients]
    elif isinstance(obj, Channel):
        return [obj.id, obj.name, obj.comment]
    elif isinstance(obj, Client):
        return [obj.admin, obj.name, obj.comment, obj.channel]
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")
