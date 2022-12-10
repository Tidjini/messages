import os
import socketio
from geventwebsocket import WebSocketServer
from geventwebsocket.handler import WebSocketHandler
from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings
from decouple import config

# django
from django.core.wsgi import get_wsgi_application

# app
from apps.communications.views import sio


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# IMPORTANT : app instead of application for vercel , make environment variable
application = get_wsgi_application()
app = application
# app = socketio.WSGIApp(sio, webapp)



# server = WebSocketServer(('localhost', 80), app)
#     # ('0.0.0.0', 8000), application, handler_class=WSGIHandler)
    
# # print('WebSocketHandler', WebSocketHandler.get_environ()['REMOTE_PORT'])

# # server = WebSocketServer(
# #     # ('0.0.0.0', 8000), application, handler_class=WSGIHandler)
# #     ('0.0.0.0', int(PORT)), app)


# server.serve_forever()


