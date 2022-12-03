import socketio

sio = socketio.Server(async_mode='gevent')

@sio.event
def connect(sid, eviron):
    print(f'Connected user <id: {sid}>')

@sio.event
def disconnect(sid):
    print(f'Disconnected user <Id: {sid}>')