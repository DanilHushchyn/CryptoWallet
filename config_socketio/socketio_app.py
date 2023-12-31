import socketio
from config_socketio.app import sio
from src.gateway.register import RegisterContainer


def create_socket_app() -> socketio.ASGIApp:
    container = RegisterContainer()
    socketio_app = socketio.ASGIApp(sio)
    socketio_app.container = container
    return socketio_app


socket_app = create_socket_app()