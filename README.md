# django-ventrilo
Django application for Ventrilo integration.

## Quickstart

_This was written to work with Django 1.4 and Python 2.7_

### Add this app to your Django ```settings.py```

    sys.path.insert(0, '/path/to/django-ventrilo')
    INSTALLED_APPS.append('ventrilo')

### Synchronize the database to add django-ventrilo tables

    $ python manage.py syncdb
    Creating tables ...
    Creating table ventrilo_server
    Creating table ventrilo_channel
    Creating table ventrilo_client
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)


### Login to the admin client and configure the ventrilo options.

- Login to the admin client (e.g. http://your-site/admin/)
- Browse to _Ventrilo_ -> _Server_
- Click the _Add_ button
- Enter the values for your Ventrilo server

### Query the status of your Ventrilo server

To get the current status of your Ventrilo server you'll need to execute the included ```update_ventrilo``` command.
When executing the command you'll need to supply a ```<HOST>``` which must match the value entered in the previous step.

    $ .venv/bin/python manage.py update_ventrilo <HOST>

To keep the information in the database up-to-date you'll want to execute this command on a schedule.
Here is a simple [Cron](https://en.wikipedia.org/wiki/Cron) entry that updates every 15 minutes.

    */15 * * * * /path/to/project/.venv/bin/python manage.py update_ventrilo vent.example.com >> /path/to/project/update_ventrilo.log

### Verify everything works

- Browse to: http://your-site/ventrilo
