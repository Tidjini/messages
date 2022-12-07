""""""
import os
import socketio
from geventwebsocket import WebSocketServer

# django
from django.core.wsgi import get_wsgi_application
from apps.communications.views import sio


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)

server = WebSocketServer(
    # ('0.0.0.0', 8000), application, handler_class=WSGIHandler)
    ('0.0.0.0', 8000), application)
server.serve_forever()
