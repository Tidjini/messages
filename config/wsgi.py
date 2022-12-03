""""""
import os
import socketio
from gevent import pywsgi
from geventwebsocket.handler import WSGIHandler

# django
from django.core.wsgi import get_wsgi_application
from apps.communications.views import sio


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)

server = pywsgi.WSGIServer(('', 8000), application, handler_class=WSGIHandler)
server.serve_forever()




