import sys	
import mod_wsgi

#set PYTHONPATH...not needed if bots is already on PYTHONPATH
sys.path.append('/srv/teaedi/backend/.env/local/lib/python2.7/site-packages')
activate_this = '/srv/teaedi/backend/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from bots import apachewebserver
import django.core.handlers.wsgi

config = mod_wsgi.process_group
apachewebserver.start(config)
application = django.core.handlers.wsgi.WSGIHandler()

