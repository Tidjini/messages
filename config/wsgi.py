""""""
import os
import socketio
from geventwebsocket import WebSocketServer

# django
from django.core.wsgi import get_wsgi_application

# app
from apps.communications.views import sio


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
web_app = get_wsgi_application()
# app instead of application for vercel
app = socketio.WSGIApp(sio, web_app)

PORT = os.environ.get('PORT', '8000')

server = WebSocketServer(
    # ('0.0.0.0', 8000), application, handler_class=WSGIHandler)
    ('0.0.0.0', 8000), app)

# server = WebSocketServer(
#     # ('0.0.0.0', 8000), application, handler_class=WSGIHandler)
#     ('0.0.0.0', int(PORT)), app)
server.serve_forever()
