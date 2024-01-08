from propan import RabbitRouter
from config_socketio.app import sio

socketio_router = RabbitRouter('socketio/')


@socketio_router.handle('send_notification')
async def send_notification(data):
    await sio.emit(event='transaction_info', data=data, room=data.get('room'))


@socketio_router.handle('update_balance')
async def update_balance(data):
    await sio.emit(event='update_balance', data=data, room=data.get('room'))


@socketio_router.handle('new_message')
async def update_balance(data):
    await sio.emit(event='new_message', data=data, room=data.get('room'))


@socketio_router.handle('update_transactions_table')
async def update_transactions_table(data):
    await sio.emit(event='update_transactions_table', data=data, room=data.get('room'))
