import os
from pathlib import Path

# django
from django.http import HttpResponse

# third_party
import socketio

# global
BASE_DIR = Path(__file__).parent
sio = socketio.Server(async_mode='gevent')
users = {}


# def index(request):
#     index_file = BASE_DIR / 'static/index.html'
#     return HttpResponse(open(index_file))


# @sio.event
# def set_username(sid, message):
#     users[sid] = message['data']
#     print(users)
#     sio.emit('my_response', {
#              'data': f'User name is set to {users[sid]}'}, to=sid)
