"""
WSGI config for settings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import os

# django
from django.core.wsgi import get_wsgi_application

# third party
import socketio

sio = socketio.Server(async_mode='gevent')

# from apps.chats.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)


server = pywsgi.WSGIServer(('', 8000), application,
                           handler_class=WebSocketHandler)

server.serve_forever()
